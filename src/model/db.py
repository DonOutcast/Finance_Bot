import sqlite3
import functools
from exception import SqlErrorsDecorator, my_decorator


class Database:

    def __init__(self, path_to_db="database.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    @SqlErrorsDecorator
    # @my_decorator
    def _execute(self, sql: str, parameters: tuple = (), fetchone=False,
                 fetchall=False, commit=False):
        connection = self.connection
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

    def crete_table_users(self):
        sql_query = """
        CREATE TABLE IF NOT EXISTS Userts (
        id int NOT NULL,
        Name varchar(255) NOT NULL,
        PRIMARY KEY(id)
        );
        """
        print(type(self._execute))
        self._execute(sql=sql_query, commit=True)


def logger(statement):
    print(f"""{statement}""")


import sys
def my_decorator(func=None, *, handle=sys.stdout):
    if func is None:
        return lambda func: my_decorator(func, handle=h)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper

@my_decorator("file.txt")
def x_and_y(x: int, y: int) -> int:
    """Hello, world!"""
    print(x + y)


if __name__ == "__main__":
    # print(x_and_y.__name__)
    # print(x_and_y.__doc__)
    # print(x_and_y.__module__)
    x_and_y(2, 2)
