import logging
import pandas as pd
from app.config import config
from app.cache import cache
from app.dataflow import helper
import threading

def _refresh()-> None:
    global WEB_SCORE
    WEB_SCORE = cache.get_cached_df(config.WEB_SCORE)
    logging.warning("Refreshing Cached Website Distribution")

def score(time: str)-> float:
    key = time
    return float(WEB_SCORE.loc[key])

_refresh()
threading.Thread(target=lambda: helper.every(config.WEB_SCORE_TTL, _refresh)).start()