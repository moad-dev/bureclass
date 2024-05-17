import polars as pl
import gzip
import subprocess

# вроде нафиг не нужно сшивать но я уже написал сорри (оно работает)
df = pl.concat(
    _.slice(1, -2)
    for _ in pl.read_excel('ksr.xlsx', engine='calamine', sheet_id=[1, 2]).values()
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


df = q.select(pl.exclude('captures')).collect()

df.write_parquet('ksr.parquet')
df.write_csv('ksr.csv')
with open('ksr.csv', 'rb') as f_in, gzip.open('ksr.csv.gz', 'wb') as f_out:
    f_out.writelines(f_in)

def get_parent_code(col: pl.Expr) -> pl.Expr:
    return (
        col
        .str.extract(r'((?:\d+[.-])+)\d+', 1)
        .str.head(-1)
    )

q = df.lazy()

def join_fold(acc, q):
    return acc.group_by(
        get_parent_code(pl.col('code')),
        maintain_order=True
    ).agg(
        childs=pl.struct(pl.exclude('code_parent'))
    ).join(
        q,
        how='left',
        left_on=pl.col('code'),
        right_on='code'
    ).select(
        'code', 'name', 'unit', 'okpd2', 'type', 'childs' 
    )




acc = q.filter(pl.col('type') == 'ресурс').with_columns(
    code_parent=pl.col('code')
)

is_machine = (
    pl.col('code').str.starts_with('96') | 
    pl.col('code').str.starts_with('91')
)
machines = acc.filter(is_machine)
not_machines = acc.filter(~is_machine)

for _ in range(5):
    not_machines = join_fold(not_machines, q)


for _ in range(4):
    machines = join_fold(machines, q)



machines.collect().write_json('machines.json', pretty=True, row_oriented=True)
not_machines.collect().write_json('not_machines.json', pretty=True, row_oriented=True)


cmd = ["jq", "-s", ".[0] +.[1]", "not_machines.json", "machines.json"]
with open("ksr.json.gz", "wb") as f:
    subprocess.run(cmd, stdout=f, check=True)
