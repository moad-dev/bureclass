import polars as pl
import os
import gzip
import pathlib

pairs_dir = pathlib.Path("pairs")
pairs_dir.mkdir(parents=True, exist_ok=True)

# Generate train-ksr pairs
q = pl.read_excel('train.xlsx', engine='calamine').lazy()

q = pl.concat([
    q.select(train='record_name', ksr='ref_name'),
    q.select(train='record_name_2', ksr='ref_name')
])

q.sink_csv('pairs/train_ksr.csv')


# Generate okpd2-ksr pairs
okpd2 = pl.scan_parquet('okpd2.parquet').select('code', 'name')
ksr = pl.scan_parquet('ksr.parquet').filter(
    pl.col('type') == 'ресурс'
).select('code', 'name', 'okpd2')

ksr.join(okpd2, left_on='okpd2', right_on='code').select(
    okpd2='name_right',
    ksr='name'
).sink_csv('pairs/okpd2_ksr.csv')


for root, dirs, files in os.walk(pairs_dir):
    for file in files:
        if file.endswith(".csv"):
            csv_file = os.path.join(root, file)
            with open(csv_file, 'rb') as f_in, gzip.open(csv_file + '.gz', 'wb') as f_out:
                f_out.writelines(f_in)
