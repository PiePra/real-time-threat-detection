import pandas as pd
from app.cache import cache
from app.config import config
import logging

def update(df: pd.DataFrame) -> None:
    df_webs = df.copy()
    counts = df_webs.groupby('activity').count()["id"]
    values=(counts / len(df))

    df_webs_scores = pd.DataFrame({"abs": counts.values, "rel": values.values, "activity": counts.index})
    df_webs_scores = df_webs_scores.sort_values("abs", ascending=False)
    df_webs_scores["cum_sum"] = df_webs_scores["rel"].cumsum()
    df_webs_scores = df_webs_scores.drop(["abs", "rel"], axis=1)
    df_webs_scores = df_webs_scores.set_index("activity", drop=True)
    cache.cache_df(config.WEB_SCORE, df_webs_scores)
    logging.warning(df_webs_scores.head(10))