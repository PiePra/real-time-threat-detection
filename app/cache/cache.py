import pandas as pd
import redis
import logging

def cache_df(alias: str, df: pd.DataFrame)-> None:
    r = redis.Redis()
    res = r.set(alias, df.to_json())
    if res == True:
        logging.warning(f'Cached Dataframe {alias}')

def get_cached_df(alias: str)-> None:
    r = redis.Redis()
    result = r.get(alias).decode()
    df = pd.read_json(result)
    return df


