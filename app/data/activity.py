import pandas as pd
import logging
import os
from app.config import config
import datetime

colnames = ["id", "date", "user", "pc", "activity"]
dev = pd.read_csv(f"{config.DATA_PREFIX}/device.csv")
http = pd.read_csv(f"{config.DATA_PREFIX}/http.csv", names=colnames, header=None)
logon = pd.read_csv(f"{config.DATA_PREFIX}/logon.csv")
dev["date"] = dev["date"].astype('datetime64[s]')
logging.warning("Formatted timestamps 1/3")
http["date"] = http["date"].astype('datetime64[s]')
logging.warning("Formatted timestamps 2/3")
logon["date"] = logon["date"].astype('datetime64[s]')
logging.warning("Formatted timestamps 3/3")
all = pd.concat([dev, http, logon]) 
all = all.drop("id", axis=1)
all = all.sort_values(by=['date'], ascending=False)
logging.warning("Imported Activity Data")

def filter_by_date(df: pd.DataFrame, days: int) -> pd.DataFrame:
    last = max(df["date"])
    df = df[df["date"] > last - datetime.timedelta(days)]
    return df