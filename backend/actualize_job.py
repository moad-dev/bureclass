import polars as pl
import os
from itertools import chain
from pathlib import Path
from elasticsearch.helpers import parallel_bulk
from elasticsearch_dsl import connections

df = pl.concat(
    _.slice(1, -2)
    for _ in pl.read_excel("data/ksr.xlsx", engine='calamine', sheet_id=[1, 2]).values()
)

df.columns = ['code', 'name', 'unit']

q = df.lazy()

q = q.with_columns(
    captures=pl.col('code').str.extract_groups(
        r'^(?<type>Книга|Часть|Раздел|Группа)? ?'
        r'(?<okpd2>\d{2}\.\d{2}\.\d{2}\.\d{3})?\.?'
        r'(?<code>\d{2}(?:\.\d{1,2})*(?:-\d{3,4})?(?:-\d{3})?):? ?'
        r'(?<name>.+)?$'
    )
)

q = q.with_columns(
    code=pl.col('captures').struct.field('code'),
    okpd2=pl.col('captures').struct.field('okpd2'),
    name=pl.when(pl.col('captures').struct.field('name').is_null())
        .then(pl.col('name'))
        .otherwise(pl.col('captures').struct.field('name')),
    type=pl.col('captures').struct.field('type').str.to_lowercase()
)    


q = q.with_columns(
    type=pl.col('type').fill_null(
        pl.when(pl.col('okpd2').is_null())
        .then(pl.lit('позиция'))
        .otherwise(pl.lit('ресурс'))
    )
)        


q = q.with_columns(
    unit=pl.when(pl.col('type').is_in(['позиция', 'ресурс']).not_())
        .then(None)
        .otherwise(pl.col('unit'))
)


new_snapshot = q.select(pl.exclude('captures')).filter(pl.col('type') == 'ресурс')

if Path("data/ksr_snapshot.parquet").exists():
    old_snapshot = pl.scan_parquet('data/ksr_snapshot.parquet')
else:
    old_snapshot = pl.LazyFrame(data=[], schema=new_snapshot.schema)

new_rows = new_snapshot.join(old_snapshot, on='code', how='anti')
deleted_rows = old_snapshot.join(new_snapshot, on='code', how='anti')
updated_rows = new_snapshot.join(old_snapshot, on='code').filter(
    (pl.col('name') != pl.col('name_right')) |
    (pl.col('okpd2') != pl.col('okpd2_right')) |
    (pl.col('unit') != pl.col('unit'))
)

# TODO: embeddings from xlsx!!!
embeddings = pl.scan_parquet('data/ksr_embeddings.parquet')

new_rows = new_rows.join(
    embeddings.select('name', 'embedding'), 
    how='left',
    on='name'
)

updated_rows = updated_rows.join(
    embeddings.select('name', 'embedding'), 
    how='left',
    on='name'
)


new_rows = new_rows.select(
    _index=pl.lit('ksr'),
    _id=pl.col('code'),
    _source=pl.struct(pl.all())
)

updated_rows = updated_rows.select(
    _op_type=pl.lit('update'),
    _id=pl.col('code'),
    doc=pl.struct(pl.exclude('code'))
)

deleted_rows = deleted_rows.select(
    _op_type=pl.lit('delete'),
    _id=pl.col('code')
)

bulk_actions = pl.collect_all(
    [new_rows, updated_rows, deleted_rows]
)

print(bulk_actions)
connections.create_connection(hosts=f"http://bureclass-search:9200", basic_auth=('elastic', os.getenv('ELASTIC_PASSWORD')))


for success, info in parallel_bulk(
    connections.get_connection(),
    chain.from_iterable(map(lambda x: x.to_dicts(), bulk_actions)),
    request_timeout=60*5,
):
    if not success:
        print('A document failed:', info)

Path("data").mkdir(exist_ok=True)
new_snapshot.collect().write_parquet('data/ksr_snapshot.parquet')
