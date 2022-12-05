import logging
import pandas as pd
from app.config import config
from app.cache import cache
from app.dataflow import helper
import threading

def _refresh()-> None:
    global USER
    USER = cache.get_cached_df(config.USER_CACHE)
    logging.warning("Refreshing Cached User List")

def get_role_from_uid(uid: str)-> str:
    return USER.loc[uid]["Role"]

_refresh()
threading.Thread(target=lambda: helper.every(config.USER_CACHE_TTL, _refresh)).start()