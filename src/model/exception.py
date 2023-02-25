from sqlite3 import Error as sql_errors
import functools


class SqlErrorsDecorator:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        try:
            result = self.func(*args, **kwargs)
            return result
        except sql_errors:
            print("Ошибка при работе с базами данных", sql_errors)


def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except sql_errors:
            print("Ошибка прои работе с базами данных", sql_errors)
    return wrapper
