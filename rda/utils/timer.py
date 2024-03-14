import functools
import time
from loguru import logger


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        logger.info(
            f"Function {func.__name__} elapsed time: {elapsed_time:0.4f} seconds"
        )
        return value, elapsed_time

    return wrapper_timer
