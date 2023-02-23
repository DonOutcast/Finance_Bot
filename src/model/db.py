import sqlite3
import functools


class Database:

    def __init__(self, path_to_db="database.db"):
        self.path_to_db = path_to_db

    @property
    def _connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False,
                fetchall=False, commit=False):
        connection = self._connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        cursor.execute(sql, parameters)
        data = None
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        elif fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    @staticmethod
    def _format_kwargs(sql: str, parameters: dict) -> tuple:
        sql += " AND".join(
            [
                f"{item} = ?" for item in parameters
            ]
        )
        return sql, tuple(parameters)


def logger(statement):
    print(f"""{statement}""")


def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except ZeroDivisionError:
            print("Деленине на ноль бро!")

    return wrapper


class MyDecorator:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        try:
            result = self.func(*args, **kwargs)
            return result
        except ZeroDivisionError:
            print("Бро тут на 0 нельзя же делить!")
        return


@MyDecorator
def summa(x, y):
    return x / y


if __name__ == "__main__":
    sqlite_connection = sqlite3.connect("d")
    cursor = sqlite_connection.cursor()
    cursor.execute("SELECT sqlite_version();")
    print(cursor.fetchone())
    cursor.close()

