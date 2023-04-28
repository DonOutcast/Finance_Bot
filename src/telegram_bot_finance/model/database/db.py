import os
import sqlite3
from typing import List, Dict
from configurate.config import DATABASE_DIR
from model.errors.exception import SqlErrorsDecorator


class Database:

    def __init__(self, path_to_db=DATABASE_DIR):
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

    def insert_item_to_table(self, table: str, column_values: Dict):
        columns = ' '.join(column_values.keys())
        values = tuple(column_values.values())
        placeholders = ", ".join("?" * len(column_values.keys()))
        sql_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self._execute(sql=sql_query, parameters=values, commit=True)

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

    def select_from_table(self, table: str, columns: List[str]):
        columns_joined = ', '.join(columns)
        sql_query = f"SELECT {columns_joined} FROM {table}"
        result = self._execute(sql=sql_query, fetchall=True)
        result = self.get_column_name_with_values(result, columns)
        return result

    def get_column_name_with_values(self, sql_data: List[tuple], columns: List[str]):
        result = []
        for row in sql_data:
            dict_row = {}
            for index, column in enumerate(columns):
                dict_row[column] = row[index]
            result.append(dict_row)
        return result


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


test_db = Database()
# test_db.drop_tables_all()
test_db.crete_table_budget()
test_db.create_table_expense()
# test_db.create_table_category()
# test_db.add_item_to_category("products", "продукты", True, "напитки")
# test_db.add_item_to_category("coffe", " кофе", True, "напитки")
# test_db.add_item_to_category("dinner", "обед", True, "столовая, бизнес-ланч")
# test_db.add_item_to_category("cafe", "кафе", True,
#                              "ресторан, рест, мак, макдональдс, макдак, kfc, ilpatio, il patio"),
# test_db.add_item_to_category("transport", "общ. транспорт", False, "метро, автобус, metro"),
# test_db.add_item_to_category("taxi", "такси", False, "яндекс такси, yandex taxi"),
# test_db.add_item_to_category("phone", "телефон", False, "теле2, связь"),
# test_db.add_item_to_category("books", "книги", False, "литература, литра, лит-ра"),
# test_db.add_item_to_category("internet", "интернет", False, "инет, inet"),
# test_db.add_item_to_category("subscriptions", "подписки", False, "подписка"),
# test_db.add_item_to_category("other", "прочее", True, "")

# test_db.select_from_table("category", "codename name is_base_expense aliases".split())
# test_db.crete_table_budget()
# test_db.create_table_category()
# test_db.drop_tables_all()
