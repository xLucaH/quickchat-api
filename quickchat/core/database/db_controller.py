import MySQLdb
from typing import List, Dict

from .connections import Connection, DjangoConnection
from . import db_utils


class Database:
    """
    Database context manager.

    @:param connection
        Pass in a Connection() class to target a specific database, either engine or django db.
    @:param use_dict_cursor
        Used to fetch the results as dictionary where each db column is the key which points to the value.
    """

    def __init__(self, connection: Connection, use_dict_cursor=False):
        self._conn = connection.get_db_connection()
        self._cursor = self._conn.cursor(MySQLdb.cursors.DictCursor) if use_dict_cursor else self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def disable_dict_cursor(self):
        self.cursor.close()
        self._cursor = self._conn.cursor()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def executemany(self, sql, params=None):
        self.cursor.executemany(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql: str, params=None, single=False):
        """
        Small helper function to easily do queries taking a shortcut and automatically doing to execute fetchall
        call that you will most likely need.

        :param sql: The SQL statement to execute.
        :param params: Parameters to insert into your "%s" placeholders.
        :param single: Will only return the first row.
        :return:
        """

        self.cursor.execute(sql, params or ())

        if not single:
            return self.fetchall()

        data = self.fetchall()

        if len(data) == 0:
            return None

        return data[0]

    def insert(self, table, data: Dict or List[Dict]):
        """
        Inserts one or multiple rows into a database table.

        :param table: Database table name.
        :param data: dictionary or list of dictionaries with key for the column names
        :return:
        """

        # Converting to a dict of lists makes it easy to use the utils method for both single and multi row inserts.
        if isinstance(data, dict):
            data = [data]

        col_names, value_placeholder, insert_values = db_utils.get_insert_formats(data)

        sql_to_execute = f"""
                         INSERT INTO {table} ({col_names})
                         VALUES {value_placeholder}
                         """

        self.execute(sql_to_execute, insert_values)
        return


class DjangoDB(Database):

    def __init__(self, *args, **kwargs):
        super().__init__(DjangoConnection(), *args, **kwargs)
