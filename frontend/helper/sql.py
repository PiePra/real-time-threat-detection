import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://digger:digger@localhost:5432/digger')
class sql():
    def __init__self():
        ""
    @staticmethod
    def getactivity():
        engine = create_engine('postgresql://digger:digger@localhost:5432/digger')
        df_raw = pd.read_sql("alerts", engine)
        return df_raw

    @staticmethod
    def delete_warning_alert(_user_id):
        engine = create_engine('postgresql://digger:digger@localhost:5432/digger')
        df_raw = pd.read_sql("alerts", engine)
        df_raw.query.filter_by(id=_user_id).delete()
        engine.session.commit()

def get_db_engine():
    DB_PASSWORD = "digger"
    DB_USER = "digger"
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "digger"
    connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_string)

