import polars as pl
import gzip

df = pl.read_excel('okpd2.xlsx', engine='calamine').slice(5)

df.columns = ['trash', 'code', 'name']

df.select('code', 'name').write_csv('okpd2.csv')
with open('okpd2.csv', 'rb') as f_in, gzip.open('okpd2.csv.gz', 'wb') as f_out:
    f_out.writelines(f_in)

