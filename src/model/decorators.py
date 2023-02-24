import types
import sys
import functools


def pre(condition, message: str):
    print(type(condition))

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            assert condition(*args, **kwargs), message
            return func(*args, **kwargs)

        return inner

    return wrapper


@pre(lambda x: x >= 0, "negative")
def checked_log(x):
    return x


if __name__ == "__main__":
    checked_log(-1)
