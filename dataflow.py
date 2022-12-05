from datetime import timedelta, datetime
import time
from bytewax.dataflow import Dataflow
from bytewax.inputs import ManualInputConfig
from bytewax.outputs import StdOutputConfig, ManualOutputConfig
from bytewax.execution import run_main, spawn_cluster, cluster_main
import pandas as pd
from bytewax import parse
from app.dataflow import timescore, webscore


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
    line["time_score"] = timescore.score(json["time"])
    if line["activity"].startswith("http"):
        line["activity_score"] = webscore.score(json["activity"])
    
    #score3
    return line

def sum_score(line):
    line["score"] = line["time_score"]# + line["activity_score"] + line["pc_score"]
    time.sleep(1)
    return line

def output_builder(worker_index: int, worker_count: int) -> callable:
    """Build the function to write to feast"""
    def write(line):
        if line["score"] > 1.4:
            return line
    return write


flow = Dataflow()
flow.input("input", ManualInputConfig(input_builder))
flow.map(get_msg)
flow.map(score)
flow.map(sum_score)
flow.capture(StdOutputConfig())

if __name__ == "__main__":
    run_main(flow)