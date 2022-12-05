import pandas as pd
from app.cache import cache
from app.config import config
import logging

def update(df: pd.DataFrame) -> None:
    df_user = df.copy()
    cache.cache_df(config.USER_CACHE, df_user)
    logging.warning(df_user.head(10))