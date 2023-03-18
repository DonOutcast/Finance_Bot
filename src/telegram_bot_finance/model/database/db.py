import os
import sqlite3
from model.errors.exception import SqlErrorsDecorator


class Database:

    def __init__(self, path_to_db="database.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    # @SqlErrorsDecorator
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

    def add_item_to_category(self, codename: str, name: str, is_base: bool, aliases: str):
        sql_query = """
        INSERT INTO category (codename, name, is_base_expense, aliases) VALUES (?, ?, ?, ?)
        """
        parameters = (codename, name, is_base, aliases)
        self._execute(sql=sql_query, parameters=parameters, commit=True)

    def crete_table_budget(self):
        sql_query = """
        CREATE TABLE IF NOT EXISTS budget (
        id int NOT NULL,
        codename varchar(255) NOT NULL,
        dily_limit integer NOT NULL,
        PRIMARY KEY(id)
        );
        """
        self._execute(sql=sql_query, commit=True)

    def create_table_category(self):
        sql_query = """
        CREATE TABLE IF NOT EXISTS category (
        id integer PRIMARY KEY AUTOINCREMENT,
        codename varchar(255),
        name varchar(255),
        is_base_expense boolean,
        aliases text
        );
        """
        self._execute(sql=sql_query, commit=True)

    def create_table_expense(self):
        sql_query = """
        CREATE TABLE IF NOT EXISTS expense (
        id integer PRIMARY KEY AUTOINCREMENT,
        amount integer,
        created datetime,
        category_codename integer,
        raw_text text,
        FOREIGN KEY(category_codename) REFERENCES category(codename)
        );
        """

    def init_budget(self):
        sql_query = """
        """
        self._execute(sql=sql_query, commit=True)

    def drop_tables_all(self):
        sql_query = """
        DROP TABLE IF EXISTS budget;
        """
        sql_query_1 = """
        DROP TABLE IF EXISTS category;
        """
        sql_query_2 = """
        DROP TABLE IF EXISTS expense;
        """
        self._execute(sql=sql_query, commit=True)
        self._execute(sql=sql_query_1, commit=True)
        self._execute(sql=sql_query_2, commit=True)


if __name__ == "__main__":
    test_db = Database()
    test_db.drop_tables_all()
    test_db.create_table_category()
    test_db.add_item_to_category("products", "продукты", True, "напитки")
    test_db.add_item_to_category("coffe", " кофе", True, "напитки")
    test_db.add_item_to_category("dinner", "обед", True, "столовая, бизнес-ланч")
    test_db.add_item_to_category("cafe", "кафе", True,
                                 "ресторан, рест, мак, макдональдс, макдак, kfc, ilpatio, il patio"),
    test_db.add_item_to_category("transport", "общ. транспорт", False, "метро, автобус, metro"),
    test_db.add_item_to_category("taxi", "такси", False, "яндекс такси, yandex taxi"),
    test_db.add_item_to_category("phone", "телефон", False, "теле2, связь"),
    test_db.add_item_to_category("books", "книги", False, "литература, литра, лит-ра"),
    test_db.add_item_to_category("internet", "интернет", False, "инет, inet"),
    test_db.add_item_to_category("subscriptions", "подписки", False, "подписка"),
    test_db.add_item_to_category("other", "прочее", True, "")

    # test_db.crete_table_budget()
    # test_db.create_table_category()
    # test_db.drop_tables_all()
