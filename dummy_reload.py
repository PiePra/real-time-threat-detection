import redis
from itertools import product
import numpy as np
from app.cache import cache
from app.config import config

df = cache.get_cached_df(config.TIMESTAMP_SCORE)


df["cum_sum"] = df["cum_sum"].apply(lambda x: np.random.random)

cache.cache_df(config.TIMESTAMP_SCORE, df)

        