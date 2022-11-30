import pandas as pd
from sqlalchemy import create_engine
import os

DB_USER = "digger"
DB_PASS = "digger"
DB_NAME = "digger"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_TYPE = "postgresql"
DATA_PREFIX = "r1"
DATA_LDAP = DATA_PREFIX + "/LDAP"

colnames = ["id", "date", "user", "pc", "activity"]
df_dev = pd.read_csv(f"{DATA_PREFIX}/device.csv")
df_http = pd.read_csv(f"{DATA_PREFIX}/http.csv", names=colnames, header=None)
df_logon = pd.read_csv(f"{DATA_PREFIX}/logon.csv")

df = pd.concat([df_dev, df_http ,df_logon ]) 
df = df.drop("id", axis=1)
df = df.sort_values(by=['date'], ascending=False)

engine = create_engine(f'{DB_TYPE}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
df.to_sql('activity', engine, index=True)

print(f"added {df.shape[0]} rows and {df.shape[1]} columns to activities database")

files = [file for file in os.listdir(DATA_LDAP)]

dfs = []
for line in files:
    df_tmp = pd.read_csv(DATA_LDAP + "/" + line)
    df_tmp["month"] = line[:-4]
    dfs.append(df_tmp)
df = pd.concat(dfs)
df.to_sql('user', engine, index=True)

print(f"added {df.shape[0]} rows and {df.shape[1]} columns to user database")