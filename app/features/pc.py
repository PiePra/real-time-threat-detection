import pandas as pd
from app.cache import cache
from app.config import config
import logging

def update(df: pd.DataFrame) -> None:
    pcs = df.copy()
    pcs = pcs.drop(["date", "activity", "domain", "employee_name", "Domain", "Email", "user"], axis=1)
    pc_scores = pcs.groupby("Role").nunique()#.sort_values(ascending=False).reset_index(name='conn_count')
    pc_scores["ratio"] = pc_scores["user_id"] / pc_scores["pc"]
    cache.cache_df(config.PC_SCORE, pc_scores)
    logging.warning(pc_scores.head(10))
    pcs["user_pc"] = pcs["user_id"] + "-" + pcs["pc"] 
    pcs = pcs.drop(["user_id", "pc"], axis=1)
    pcs = pcs.drop_duplicates("user_pc")
    pcs = pcs.set_index("user_pc", drop=True)
    logging.warning(pcs.head(10))
    cache.cache_df(config.USER_PC_LIST, pcs)