import logging
import pandas as pd
from app.config import config
from app.cache import cache
from app.dataflow import helper
import threading

def _refresh()-> None:
    global TIMESTAMP_SCORE
    TIMESTAMP_SCORE = cache.get_cached_df(config.TIMESTAMP_SCORE)
    logging.warning("Refreshing Cached Timestamp Distribution")
        
def _format(time: str) -> str:
    time = pd.to_datetime(time)
    day = str(time.weekday())
    hour = str(time.hour)
    return day + "-" + hour

def score(time: str)-> float:
    key = _format(time)
    return float(TIMESTAMP_SCORE.loc[key])

_refresh()
threading.Thread(target=lambda: helper.every(config.TIMESTAMP_SCORE_TTL, _refresh)).start()