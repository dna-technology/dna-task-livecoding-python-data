import sqlite3

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = self._connect()
        self.create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id TEXT PRIMARY KEY,
                merchant_id TEXT,
                amount INT,
                currency TEXT,
                payment_method TEXT,
                date TEXT
            )
        """)
        self.conn.commit()

    def get_connection(self):
        return self.conn