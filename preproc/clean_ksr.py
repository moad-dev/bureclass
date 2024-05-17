import polars as pl
import gzip

q = pl.scan_parquet('ksr.parquet')

q.filter(
    pl.col('type') == 'ресурс'
).select(
    pl.concat_str(pl.col('okpd2'), pl.lit('.'), pl.col('code')),
    pl.col('name'),
    pl.col('unit')
).sink_csv('ksr_clean.csv')

with open('ksr_clean.csv', 'rb') as f_in, gzip.open('ksr_clean.csv.gz', 'wb') as f_out:
    f_out.writelines(f_in)
