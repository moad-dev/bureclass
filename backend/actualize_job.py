import polars as pl
import os
from itertools import chain
from pathlib import Path
from elasticsearch.helpers import bulk
from elasticsearch_dsl import connections

<<<<<<< HEAD
def actualize_job():
    df = pl.concat(
        _.slice(1, -2)
        for _ in pl.read_excel('data/ksr.xlsx', engine='calamine', sheet_id=[1, 2]).values()
=======
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
>>>>>>> 05eda68d6927cdc2d22d0ba017be79eca033e92c
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


new_snapshot = q.select(pl.exclude('captures'))

if Path("data/ksr_snapshot.parquet").exists():
    old_snapshot = pl.scan_parquet('data/ksr_snapshot.parquet')
else:
    old_snapshot = pl.LazyFrame(data=[], schema=new_snapshot.schema)

new_rows = new_snapshot.join(old_snapshot, on='code', how='anti')
deleted_rows = old_snapshot.join(new_snapshot, on='code', how='anti')
updated_rows = new_snapshot.join(old_snapshot, on='code').filter(
    (pl.col('name') != pl.col('name_right')) |
    (pl.col('okpd2') != pl.col('okpd2_right')) |
    (pl.col('okpd2') != pl.col('okpd2_right')) |
    (pl.col('unit') != pl.col('unit'))
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

bulk_actions = pl.collect_all([new_rows, updated_rows, deleted_rows])


connections.create_connection(hosts=f"http://search:9200", basic_auth=('elastic', os.getenv('ELASTIC_PASSWORD')))

bulk(
    connections.get_connection(),
    chain.from_iterable(map(lambda df: df.to_dicts(), bulk_actions))
)

Path("data").mkdir(exist_ok=True)
new_snapshot.collect().write_parquet('data/ksr_snapshot.parquet')
