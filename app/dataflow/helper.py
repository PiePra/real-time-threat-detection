import time
from typing import Callable

def every(delay: int, func: Callable):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        func()
        next_time += (time.time() - next_time) // delay * delay + delay