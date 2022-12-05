import pandas as pd
import os
import logging
from app.config import config

files = [file for file in os.listdir(config.DATA_LDAP)]

dfs = []
for line in files:
    df_tmp = pd.read_csv(config.DATA_LDAP + "/" + line)
    df_tmp["month"] = line[:-4]
    dfs.append(df_tmp)
user = pd.concat(dfs)
user = user.drop("month", axis=1)
user = user.drop_duplicates()
user = user.set_index("user_id")
user = user
logging.warning("Imported User Data")

def join_on_uid(df: pd.DataFrame) -> pd.DataFrame:
    df[['domain', 'user_id']] = df['user'].str.split('/', 1, expand=True)
    df = df.join(user, on="user_id")    
    return df