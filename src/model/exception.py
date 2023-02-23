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
        return

