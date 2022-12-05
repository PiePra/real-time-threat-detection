import logging
import pandas as pd
from app.config import config
from app.cache import cache
from app.dataflow import helper
import threading

def _refresh()-> None:
    global DEVICE_SCORE
    DEVICE_SCORE = cache.get_cached_df(config.DEVICE_SCORE)
    logging.warning("Refreshing Cached Device Connection Distribution")

def score(key: str)-> str:
    ratio = DEVICE_SCORE.loc[key]["ratio"]
    return  1 * (1 - (3 * ratio))

_refresh()
threading.Thread(target=lambda: helper.every(config.DEVICE_SCORE_TTL, _refresh)).start()