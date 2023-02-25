import os
import sys
import json
import types
import typing
import functools
import logging
import logging.config

log_config = {
    "version": 1,
    "formatters": {
        "primes_formatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "main_formatter": {
            "format": "%(asctime)s - %(message)s",
            "datefmt": "%d/%m/%Y"

        },
    },
    "handlers": {
        "primes_handler": {
            "class": "logging.FileHandler",
            "formatter": "primes_formatter",
            "filename": "primes.log",
            "encoding": "UTF-8"
        },
        "main_handler": {
            "class": "logging.FileHandler",
            "formatter": "main_formatter",
            "filename": "main.log",
            "encoding": "UTF-8",
        },
    },
    "loggers": {
        "primes": {
            "handlers": ["primes_handler"],
            "level": "DEBUG",
        },
        "main": {
            "handlers": ["main_handler"],
            "level": "INFO",
        }
    }
}



class Logger:

    def __init__(self, name: str, filename: str):
        self.name = name
        self.filename = filename
        self.logger = None

    def __configurate_logger(self):
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(self.filename, "a", "utf-8")
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(messsage)s")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        self.__configurate_logger()
        return self.logger


# def decorator(message):
#     def wrapper(func):
#         def inner(*args, **kwargs):
#             logger = Logger("shamil", "info.log")
#             logger.info(f"Function name: {func.__name__}, function called {func.__module__}")
#             result = func(*args, **kwargs)
#             return result
#
#         return inner
#
#     return wrapper


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
# @decorator("Hello world")
# def checked_log(x):
#     return x


if __name__ == "__main__":
    # logging.config.dictConfig(log_config)
    # log = logging.getLogger("primes")
    # log.debug("Hello")
    # log_1 = logging.getLogger("main")
    # log_1.info("World")
    with open('../configurate/log_config.json') as f:
        data = json.load(f)

    print(data)