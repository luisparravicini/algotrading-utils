from datetime import datetime
import ccxt
import time
from pathlib import Path
import re
from .db import Database


class Updater:
    def __init__(self, exchange_name, symbol, db_base_path):
        self.exchange_name = exchange_name
        exchange = getattr(ccxt, exchange_name)
        self.exchange = exchange({
            'enableRateLimit': True
        })

        self.symbol = symbol

        self.db_base_path = db_base_path

        name = re.sub(r'\W', '_', exchange_name + '_' + symbol) + '.db'
        name = name.lower()
        self.db_path = Path(self.db_base_path).joinpath(name)
        self.db = Database(self.db_path)


    def fetch_ohlcv(self):
        since = self.db.newest_timestamp()
        # some exchanges use since as an exclusive limit
        # we ask again for the last candle in case the last time we
        # got that data, it was not closed yet and contained partial data
        if since is not None:
            since -= 1

        data = self.exchange.fetch_ohlcv(self.symbol, timeframe='1m', since=since)

        self.converts_timestamp_to_seconds(data)
        return data


    def converts_timestamp_to_seconds(self, data):
        for datum in data:
            datum[0] = datum[0] // 1000


    def fetch_and_save(self):
        data = self.fetch_ohlcv()

        if len(data) > 0:
            self.db.add(data)

        for datum in data:
            date = datetime.fromtimestamp(datum[0]).strftime('%Y-%m-%d %H:%M:%S')
            print(date, datum)


    def run(self):
        while True:
            self.fetch_and_save()

            time.sleep(45)
