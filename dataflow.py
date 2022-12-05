from datetime import timedelta, datetime
import time
from bytewax.dataflow import Dataflow
from bytewax.inputs import ManualInputConfig
from bytewax.outputs import StdOutputConfig, ManualOutputConfig
from bytewax.execution import run_main, spawn_cluster, cluster_main
import pandas as pd
from bytewax import parse
from app.dataflow import timescore, webscore, user, devicescore, pcscore


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
    json["activity"] = json["activity"].strip()
    json["user_id"] = json["user_id"][5:]
    return json

def get_role(json):
    json["role"] = user.get_role_from_uid(json["user_id"])
    return json

def score_time(json):
    json["time_score"] = timescore.score(json["time"])
    return json

def score_activity(json):
    if json["activity"].startswith("http"):
        json["activity_score"] = webscore.score(json["activity"])
    elif json["activity"] == "Connect":
        json["activity_score"] = devicescore.score(json["role"])
    else:
        json["activity_score"] = 0
    return json

def score_pc(json):
    json["pc_score"] = pcscore.score(json["user_id"], json["pc"], json["role"])
    return json

def sum_score(json):
    json["score"] = json["time_score"] + json["activity_score"] + json["pc_score"]
    #time.sleep(1)
    return json

def output_builder(worker_index: int, worker_count: int) -> callable:
    """Build the function to write to feast"""
    def write(json):
        if json["score"] > 2.5:
            print(json) 
    return write


flow = Dataflow()
flow.input("input", ManualInputConfig(input_builder))
flow.map(get_msg)
flow.map(get_role)
flow.map(score_time)
flow.map(score_activity)
flow.map(score_pc)
flow.map(sum_score)
flow.capture(ManualOutputConfig(output_builder))

if __name__ == "__main__":
    run_main(flow)