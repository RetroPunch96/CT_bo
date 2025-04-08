import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self, path='trades.db'):
        self.path = path
        self._init_db()

    def _init_db(self):
        with self.connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    id TEXT PRIMARY KEY,
                    symbol TEXT,
                    side TEXT,
                    amount REAL,
                    entry_price REAL,
                    exit_price REAL,
                    timestamp DATETIME
                )
            """)

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.path)
        try:
            yield conn
        finally:
            conn.close()
