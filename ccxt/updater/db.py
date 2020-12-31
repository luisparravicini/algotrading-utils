import sqlite3


class Database:
    def __init__(self, path):
        self.path = path
        new_db = not path.exists()
        self.conn = sqlite3.connect(self.path)

        if new_db:
            self.conn.execute('''
                CREATE TABLE ohlcv (
                    timestamp INTEGER PRIMARY KEY ASC,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume REAL);
            ''')

    def add(self, data):
        self.conn.executemany('''
            INSERT OR REPLACE INTO ohlcv
            (timestamp, open, high, low, close, volume)
            VALUES
            (?, ?, ?, ?, ?, ?)
        ''', data)
        self.conn.commit()

    def newest_timestamp(self):
        cursor = self.conn.execute('SELECT MAX(timestamp) FROM ohlcv')
        data = cursor.fetchone()[0]
        cursor.close()

        return data
