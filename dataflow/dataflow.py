from datetime import timedelta, datetime

from bytewax.dataflow import Dataflow
from bytewax.inputs import ManualInputConfig
from bytewax.outputs import StdOutputConfig, ManualOutputConfig
from bytewax.execution import run_main, spawn_cluster, cluster_main
from bytewax.window import SystemClockConfig, TumblingWindowConfig
from sqlalchemy import create_engine
import pandas as pd
import requests
from bytewax import parse


def input_builder(worker_index, worker_count, resume_state):
    state = None # ignore recovery
    for line in open("sample.csv"):
        yield state, line

def get_msg(line):
    list = line.split(",")
    json = {
        "id": list[0],
        "time": list[1],
        "user_id": list[2],
        "pc": list[3],
        "activity": list[4],
    }
    return json

def score(line):
    json = line.copy()
    del json["id"]
    json["activity"] = json["activity"].strip()
    r = requests.post("http://localhost:8000/check", json=json)
    r = r.json()
    line["time_score"] = r["time_score"]
    line["pc_score"] = r["pc_score"]
    line["activity_score"] = r["activity_score"]
    return line

def sum_score(line):
    line["score"] = line["time_score"] + line["activity_score"] + line["pc_score"]
    return line

def _get_db_engine():
    DB_PASSWORD = "digger"
    DB_USER = "digger"
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "digger"
    connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_string)

def output_builder(worker_index: int, worker_count: int) -> callable:
    """Build the function to write to feast"""
    engine = _get_db_engine()
    def write(line):
        if line["score"] > 1.4:
            df = pd.DataFrame([line])
            df.to_sql("alerts", engine, if_exists='append', index=False)
    return write


flow = Dataflow()
flow.input("input", ManualInputConfig(input_builder))
flow.map(get_msg)
flow.map(score)
flow.map(sum_score)
#flow.capture(StdOutputConfig())
flow.capture(ManualOutputConfig(output_builder))
#args = "-w1 -n4".split()

if __name__ == "__main__":
    run_main(flow)
    #spawn_cluster(flow, **parse.cluster_args(args))