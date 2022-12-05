import pandas as pd
from app.cache import cache
from app.config import config
import logging

def update(df: pd.DataFrame) -> None:
    activity = df.copy()
    activity = activity.drop(["date", "pc", "domain", "user_id", "employee_name", "Domain", "Email"], axis=1)
    activity_score = activity.groupby("Role")["activity"].count().sort_values(ascending=False).reset_index(name='conn_count')
    length_connect = len(activity)
    activity_score["ratio"] = activity_score["conn_count"] / length_connect
    activity_score = activity_score.set_index("Role")
    cache.cache_df(config.DEVICE_SCORE, activity_score)
    logging.warning(activity_score.head(10))