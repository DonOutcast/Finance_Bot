import sqlite3
from model.errors.exception import SqlErrorsDecorator


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

    # def crete_table_users(self):
    #     sql_query = """
    #     CREATE TABLE IF NOT EXISTS Userts (
    #     id int NOT NULL,
    #     Name varchar(255) NOT NULL,
    #     PRIMARY KEY(id)
    #     );
    #     """
    #     print(type(self._execute))
    #     self._execute(sql=sql_query, commit=True)

