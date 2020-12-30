import sqlite3


class Database:
    def __init__(self, path):
        self.path = path

# CREATE TABLE ohlcv (
#     timestamp INTEGER PRIMARY KEY ASC,
#     open REAL,
#     high REAL,
#     low REAL,
#     close REAL,
#     volume REAL);
