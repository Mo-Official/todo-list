from configparser import ConfigParser
from psycopg2._psycopg import connection
import psycopg2


class PostgreConnector:
    conn: connection
    db_type = "postgresql"

    def __init__(self, config_file, schema=...) -> None:
        "builds connection to db"
        self.schema = "public" if schema == ... else schema
        parser = ConfigParser()
        parser.read(config_file)
        self.configs = {}
        if parser.has_section(self.db_type):
            params = parser.items(self.db_type)
            for param in params:
                self.configs[param[0]] = param[1]
            try:
                self.conn = psycopg2.connect(**self.configs)
            except (psycopg2.DatabaseError, Exception) as error:
                raise (error)

        else:
            raise Exception(
                f"Configuration File not working: Section {self.db_type} not found in the {config_file} file"
            )

    def update_task(self, id, value):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE tasks SET title = %s WHERE id = %s;", (value, id))
            self.conn.commit()
        except (psycopg2.DatabaseError, Exception) as err:
            self.conn.rollback()
            raise (err)

    def add_task(self, value):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO tasks(title) VALUES (%s);", (value,))
            self.conn.commit()
        except (psycopg2.DatabaseError, Exception) as err:
            self.conn.rollback()
            raise (err)

    def delete_task(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = %s;", id)
            self.conn.commit()
        except (psycopg2.DatabaseError, Exception) as err:
            self.conn.rollback()
            raise (err)

    def get_task(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, title FROM tasks WHERE id = %s;", id)
            return cursor.fetchone()
        except (psycopg2.DatabaseError, Exception) as err:
            raise (err)

    def get_tasks(self, title):
        try:
            cursor = self.conn.cursor()
            if title == "*":
                cursor.execute("SELECT id, title FROM tasks;")
            else:
                cursor.execute("SELECT id, title FROM tasks WHERE title = %s;", title)
            return cursor.fetchall()
        except (psycopg2.DatabaseError, Exception) as err:
            raise (err)

    def close_connection(self):
        if self.conn.closed == 0:
            self.conn.close()
