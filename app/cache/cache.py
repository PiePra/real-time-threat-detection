import pandas as pd
import redis
import logging

def cache_df(alias,df):
    r = redis.Redis()
    res = r.set(alias, df.to_json())
    if res == True:
        logging.warning(f'Cached Dataframe {alias}')

def get_cached_df(alias):
    r = redis.Redis()
    result = r.get(alias).decode()
    df = pd.read_json(result)
    return df


