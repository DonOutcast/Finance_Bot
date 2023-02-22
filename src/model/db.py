import sqlite3


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






