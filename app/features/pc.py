import pandas as pd
from app.cache import cache
from app.config import config
import logging

def run_scoring(df: pd.DataFrame) -> None:
    pcs = df.copy()
    pcs = pcs.drop(["date", "activity", "domain", "employee_name", "Domain", "Email", "user"], axis=1)
    pc_scores = pcs.groupby("Role").nunique()#.sort_values(ascending=False).reset_index(name='conn_count')
    pc_scores["ratio"] = pc_scores["user_id"] / pc_scores["pc"]
    cache.cache_df(config.PC_SCORE, pc_scores)
    logging.warning(pc_scores.head(10))
