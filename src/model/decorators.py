import os
import sys
import types
import typing

import functools
import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    filename='example.log',
    encoding='utf-8',
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)
logger = logging.getLogger("Shamil")


def decorator(message):
    def wrapper(func):
        def inner(*args, **kwargs):
            logger.debug(f"Function name: {func.__name__}, function called {func.__module__}")
            result = func(*args, **kwargs)
            return result

        return inner

    return wrapper


def pre(condition: typing.Callable, message: str):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            assert condition(*args, **kwargs), message
            result = func(*args, **kwargs)
            return result

        return inner

    return wrapper


def post(condition: typing.Callable, message: str):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            assert condition(*args, **kwargs), message
            return result

        return inner

    return wrapper


# @pre(lambda x: x >= 0, "negative")
@decorator("Hello world")
def checked_log(x):
    return x


if __name__ == "__main__":
    checked_log(1)
