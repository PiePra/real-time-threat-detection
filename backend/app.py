from fastapi import FastAPI
from pydantic import BaseModel
import datetime
import pandas as pd
from sklearn import preprocessing
from sqlalchemy import create_engine
import logging

app = FastAPI()

class Item(BaseModel):
    user_id: str
    pc: str
    time: str
    activity: str

def _get_db_engine():
    DB_USER = "digger"
    DB_PASS = "digger"
    DB_NAME = "digger"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_TYPE = "postgresql"
    connection_string = f'{DB_TYPE}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    return create_engine(connection_string)

def _get_data(engine, table_name) -> pd.DataFrame:
    return pd.read_sql(table_name, engine)

def _format_index():
    app.df = app.df.reset_index(drop=True)
    app.df = app.df.drop("index", axis=1)
    app.user = app.user.reset_index(drop=True)
    app.user = app.user.drop("index", axis=1)

def _join_role_activity():
    app.user = app.user.drop("month", axis=1)
    app.user = app.user.drop_duplicates()
    app.df[['domain', 'user_id']] = app.df['user'].str.split('/', 1, expand=True)
    app.user = app.user.set_index("user_id")
    app.df = app.df.join(app.user, on="user_id")

def _filter_df_by_time(df, days=30):
    df["date"] = pd.to_datetime(df["date"])
    last = max(df["date"])
    df = df[df["date"] > last - datetime.timedelta(days) ]
    
def _init_data():
    logging.info("Startup event")
    engine = _get_db_engine()
    logging.info("Loaded DB Config")
    app.user = _get_data(engine, "user")
    logging.info("Polled User Data")
    app.df = _get_data(engine, "activity")
    logging.info("Polled Activity Data")
    _format_index()
    logging.info(f"Indexed {len(app.df)} items")
    _join_role_activity()    
    logging.info("Joined User Roles")
    
#time srv
def _get_day_hour():
    app.df_time["date"] = app.df_time["date"].astype('datetime64[s]')
    app.df_time["day"] = app.df_time["date"].apply(lambda x: x.weekday())
    app.df_time["hour"] = app.df_time["date"].apply(lambda x: x.hour)
    app.df_time_stats = app.df_time.copy()
    app.df_time["day-hour"] = app.df_time["day"].astype("string") + "-" + app.df_time["hour"].astype("string")
    app.df_time.drop(["date", "day", "hour"], axis=1)

#time srv
def _label_encode():
    le = preprocessing.LabelEncoder()
    le.fit(app.df_time["Role"])
    app.df_time["role"] = le.transform(app.df_time["Role"])
    app.df_time.drop("Role", axis=1)

#time srv
def _get_distribution():
    app.df_time = app.df_time.drop(["Email", "employee_name", "domain", "Domain", "pc", "activity", "user_id", "user"], axis=1)
    counts = app.df_time.groupby("day-hour").count()["role"]
    values=(counts / len(app.df_time))
    app.df_final = pd.DataFrame({"abs": counts.values, "rel": values.values, "day-hour": counts.index})
    app.df_final = app.df_final.sort_values("abs", ascending=False)
    app.df_final = app.df_final.reset_index(drop=True)
    app.df_final["cum_sum"] = app.df_final["rel"].cumsum()
    app.p70 = app.df_final[app.df_final["cum_sum"] > 0.7]
    app.p85 = app.df_final[app.df_final["cum_sum"] > 0.85]
    app.p95 = app.df_final[app.df_final["cum_sum"] > 0.95]

def _get_role_from_user_id(id):
    return app.user.loc[id]["Role"]
    
#time srv
def _transform_time_input(item):
    time = pd.to_datetime(item.time)
    day = str(time.weekday())
    hour = str(time.hour)
    return day + "-" + hour

async def _refit_all():
    _init_data()
    _pc_refit()
    _time_refit()
    _activity_refit()

def _time_refit():
    app.df_time = app.df.copy()
    logging.info("Loaded new Data")
    _get_day_hour()
    logging.info("Converted Datetime to Day and Hour")
    _label_encode()
    logging.info("Encoded Labels")
    _get_distribution()
    logging.info("Updated Distribution")

def _time_check(item):
    input = _transform_time_input(item)
    if input in app.p95["day-hour"].values:
        return 0.9
    elif input in app.p85["day-hour"].values:
        return 0.5
    elif input in app.p70["day-hour"].values:
        return 0.3
    else:
        return 0

# global
@app.on_event("startup")
async def startup_event():
   await _refit_all()
    
@app.post("/time-check")
async def time_check(item: Item) -> int:
    return _time_check(item)

@app.get("/time-refit")
async def time_refit():
    _init_data()
    _time_refit()


@app.get("/time-statistics")
async def time_statistics():
    return app.df_time_stats[["day", "hour"]].to_json()



#user-pc

def _get_user_pc_pairs(df):
    df = df.drop(["date", "activity", "domain", "employee_name", "Domain", "Email"], axis=1)
    df = df.drop_duplicates()
    app.user_pc_pairs = df.copy()
    app.user_pc_pairs = app.user_pc_pairs.drop("Role", axis=1)
    app.user_pc_pairs["user-pc"] = app.user_pc_pairs["user_id"] + "-" + app.user_pc_pairs["pc"]
    app.user_pc_pairs = pd.Series(app.user_pc_pairs["user-pc"])

def _get_role_volatility_factor(df):
    app.factors = df.groupby("Role").nunique()
    app.factors["factor"] = app.factors["user_id"] / app.factors["pc"]
    app.factors = app.factors.drop(["user", "user_id", "pc"], axis=1)

def _get_factor_from_role(role):
    return app.factors.loc[role]["factor"]

def _pc_refit():
    logging.info("Joined User Roles")
    app.df_pc = app.df.copy()
    _filter_df_by_time(app.df_pc, days = 30)
    logging.info("Removed older values from dataframe")
    _get_user_pc_pairs(app.df_pc)
    logging.info("Created unique pc-user pairs")
    _get_role_volatility_factor(app.df_pc)
    logging.info("Calculated volatility factor for Roles")

def _pc_check(item):
    user = item.user_id.split("/")[1]
    user_pc = user + "-" + item.pc
    if user_pc in app.user_pc_pairs.values:
        score = 0
    else:
        role = _get_role_from_user_id(user)
        factor = _get_factor_from_role(role)
        score = 1 * (1 - factor)
    return score

@app.post("/pc-check")
async def pc_check(item: Item) -> int:
    return _pc_check(item)
    
          
@app.get("/pc-refit")
async def pc_refit():
    _init_data()
    _pc_refit()
    
@app.get("/pc-role-factors")
async def pc_role_factors() -> int:
    return app.factors.to_json()

@app.get("/pc-unique-connections")
async def pc_unique_connections() -> int:
    return app.user_pc_pairs.to_json()

# activity

def _get_logOff_count(groupClasue) -> pd.DataFrame:
    df_logoff = app.df_activity.loc[app.df_activity['activity'] == 'Logoff']
    df_loffcount = df_logoff.groupby(groupClasue)['activity'].count().reset_index(name='count_logoff')
    return df_loffcount

def _get_device_count(groupClasue) -> pd.DataFrame:
    df_connect = app.df_activity.loc[app.df_activity['activity'] == 'Connect']
    df_conncount = df_connect.groupby(groupClasue)['activity'].count().reset_index(name='count_connect')
    return df_conncount

def _get_unique_web_count(groupClasue) -> pd.DataFrame:
    df_http = app.df_activity.loc[app.df_activity['activity'].str.startswith("http")]
    df_sites = df_http.loc[(df_http['activity'].str.startswith('http://wikileaks')) | (df_http['activity'].str.startswith('http://linkedin'))]
    df_sitescount = df_sites.groupby(groupClasue)['activity'].value_counts().reset_index(name='count_sus_site')
    df_sitescount.drop('activity', axis =1, inplace = True)
    return df_sitescount

def _get_web_count(groupClasue) -> pd.DataFrame:
    df_http = app.df_activity.loc[app.df_activity['activity'].str.startswith("http")]
    df_webcount = df_http.groupby(groupClasue)['activity'].count().reset_index(name='count_http')
    return df_webcount

def _join_stats(groupClasue) -> pd.DataFrame:
    df_lcount = _get_logOff_count(groupClasue)
    df_ccount = _get_device_count(groupClasue)
    df_wcount = _get_web_count(groupClasue)
    df_uwcount = _get_unique_web_count(groupClasue)
    dfs = [df_lcount, df_ccount, df_uwcount, df_wcount]
    #Set Index
    dfs = [df.reset_index(drop = True) for df in dfs]
    dfs = [df.set_index(groupClasue) for df in dfs]
    
    df_join = dfs[0].join(dfs[1:], how='left')
    return df_join

def _check_http(url):
    if url in app.url_p98.index.values or url not in app.url_all.index.values:
        score = 0.9
    elif url in app.url_p96.index.values:
        score = 0.6
    elif url in app.url_p94.index.values:
        score = 0.3
    else:
        score = 0
    return score

def _get_ratio_from_role(user_id):
    user = user_id.split("/")[1]
    role = _get_role_from_user_id(user)
    return app.df_activity_score.loc[role]["ratio"]

def _activity_refit():
    app.df_activity = app.df.copy()
    _filter_df_by_time(app.df_activity, days=120)
    app.df_http_activity = app.df_activity.copy()
    app.df_device_activity = app.df_activity.copy()
    app.df_role_data = _join_stats(['Role'])
    logging.info("Data prepared")
    app.df_activity = app.df_activity[app.df_activity["activity"].str.startswith("http")]
    app.df_activity = app.df_activity.drop(["date", "pc", "domain", "user_id", "employee_name", "Domain", "Email", "Role"], axis=1)
    length = len(app.df_activity)
    df_score = pd.DataFrame(app.df_activity.groupby("activity")["activity"].count().sort_values(ascending=False))
    df_score["ratio"] = df_score["activity"] / length
    df_score["cumsum"] = df_score["ratio"].cumsum()
    app.url_p94 = df_score[ df_score["cumsum"] > 0.94 ] 
    app.url_p96 = df_score[ df_score["cumsum"] > 0.96 ] 
    app.url_p98 = df_score[ df_score["cumsum"] > 0.98 ]
    app.url_all = df_score
    app.df_device_activity = app.df_device_activity[app.df_device_activity["activity"] == 'Connect']
    app.df_device_activity = app.df_device_activity.drop(["date", "pc", "domain", "user_id", "employee_name", "Domain", "Email"], axis=1)
    df_score_connect = app.df_device_activity.groupby("Role")["activity"].count().sort_values(ascending=False).reset_index(name='conn_count')
    length_connect = len(app.df_device_activity)
    df_score_connect["ratio"] = df_score_connect["conn_count"] / length_connect
    df_score_connect = df_score_connect.set_index("Role")
    app.df_activity_score = df_score_connect

def _activity_check(item):
    if item.activity.startswith("http://") or item.activity.startswith("https://"):
        score = _check_http(item.activity)
    elif item.activity.startswith("Connect"):
        #_check_device()
        ratio = _get_ratio_from_role(item.user_id)
        score = 1 * (1 - (3 * ratio))
    else:
        score = 0
    return score

@app.post("/activity-check")
async def activity_check(item: Item) -> int:
    return _activity_check(item)

@app.get("/activity-refit")
async def activity_refit():
    _init_data()
    _activity_refit()

@app.post("/check")
async def check(item: Item) -> int:
    out = {"pc_score": _pc_check(item),
           "activity_score": _activity_check(item),
           "time_score": _time_check(item)}
    return out

@app.get("/activity-statistics")
async def activity_statistics() -> int:
    return app.df_role_data.to_json()

@app.get("/activity-ratios")
async def activity_ratios() -> int:
    return app.df_activity_score.to_json()


@app.get("/all-refit")
async def refit_all() -> int:
    _refit_all()