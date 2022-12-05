import pandas as pd
from app.cache import cache
from app.config import config
import logging


def update(df: pd.DataFrame) -> None:
    df_timestamps = df.copy()
    df_timestamps["day"] = df_timestamps["date"].apply(lambda x: x.weekday())
    df_timestamps["hour"] = df_timestamps["date"].apply(lambda x: x.hour)
    df_timestamps["day-hour"] = df_timestamps["day"].astype("string") + "-" + df_timestamps["hour"].astype("string")
    counts = df_timestamps.groupby("day-hour").count()["date"]
    values=(counts / len(df))

    df_time_scores = pd.DataFrame({"abs": counts.values, "rel": values.values, "day-hour": counts.index})
    df_time_scores = df_time_scores.sort_values("abs", ascending=False)
    df_time_scores["cum_sum"] = df_time_scores["rel"].cumsum()
    df_time_scores = df_time_scores.drop(["abs", "rel"], axis=1)
    df_time_scores = df_time_scores.set_index("day-hour", drop=True)
    cache.cache_df(config.TIMESTAMP_SCORE, df_time_scores)
    logging.warning(df_time_scores.head(10))

