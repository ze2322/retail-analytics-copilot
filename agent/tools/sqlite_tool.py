<<<<<<< HEAD
import sqlite3

class SQLiteTool:
    def __init__(self, db_path="data/northwind.sqlite"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def run_query(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = [dict(row) for row in cursor.fetchall()]
            return rows, None
        except Exception as e:
            return None, str(e)
=======
import sqlite3

class SQLiteTool:
    def __init__(self, db_path="data/northwind.sqlite"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def run_query(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = [dict(row) for row in cursor.fetchall()]
            return rows, None
        except Exception as e:
            return None, str(e)
>>>>>>> 8e017c34374abf24b249e7e3dbbfa14b453c5c75
