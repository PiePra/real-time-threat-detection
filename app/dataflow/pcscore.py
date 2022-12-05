import logging
import pandas as pd
from app.config import config
from app.cache import cache
from app.dataflow import helper
import threading

def _refresh_pc_score()-> None:
    global PC_SCORE
    PC_SCORE = cache.get_cached_df(config.PC_SCORE)
    logging.warning("Refreshing Cached PC Usage Distribution")

def _refresh_user_pc_list()-> None:
    global USER_PC_LIST
    USER_PC_LIST = cache.get_cached_df(config.USER_PC_LIST)
    logging.warning("Refreshing Cached User PC List")

def _format(user: str, pc: str) -> str:
    return user + "-" + pc

def score(user: str, pc: str, role: str)-> float:
    key = _format(user, pc)
    if key in USER_PC_LIST.index:
        return 0
    else:
        ratio = PC_SCORE.loc[role]["ratio"]
        return 2 * ratio

_refresh_pc_score()
threading.Thread(target=lambda: helper.every(config.PC_SCORE_TTL, _refresh_pc_score)).start()
_refresh_user_pc_list()
threading.Thread(target=lambda: helper.every(config.USER_PC_LIST_TTL, _refresh_user_pc_list)).start()