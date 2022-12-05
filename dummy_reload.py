import redis
from itertools import product
import numpy as np

r = redis.Redis()

DAYS = [i for i in range(0,7)]
HOURS = [i for i in range(0,24)]
TIMESTAMP_SCORES = {}

def reload():
    keys = list(product(DAYS, HOURS))
    for item in keys:
        key = f"{item[0]}-{item[1]}"
        val = np.random.random(1)[0]
        TIMESTAMP_SCORES[key] = val if val else 0
reload()
r.mset(TIMESTAMP_SCORES)

        