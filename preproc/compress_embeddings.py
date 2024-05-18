import pickle
import polars as pl


with open('ksr_embeddings_advanced.pkl', 'rb') as f:
    df = pickle.load(f)
    
    pl.from_pandas(df).write_parquet('ksr_embeddings_advanced.parquet')
