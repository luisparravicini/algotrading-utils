import sqlite3
from contextlib import closing
from pathlib import Path
import re


class Database:
    def __init__(self, exchange_name, symbol, base_path):
        self.path = self._build_name(exchange_name, symbol, base_path)
        new_db = not self.path.exists()
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


    def _build_name(self, exchange_name, symbol, base_path):
        name = re.sub(r'\W', '_', exchange_name + '_' + symbol) + '.db'
        name = name.lower()
        return Path(base_path).joinpath(name)

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

    def fetch_timestamps(self):
        query = 'SELECT timestamp FROM ohlcv ORDER BY timestamp ASC'
        with closing(self.conn.execute(query)) as cursor:
            for row in cursor:
                yield row[0]

