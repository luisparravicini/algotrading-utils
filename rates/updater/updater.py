from datetime import datetime
import ccxt
import time
import re
from .db import Database
from .exchange import build_exchange, timestamps_to_seconds, secs_to_millis


class Updater:
    def __init__(self, exchange_name, symbol, db_base_path):
        self.exchange = build_exchange(exchange_name)
        self.symbol = symbol
        self.db = Database(exchange_name, self.symbol, db_base_path)
        self.sleep_time = 45


    def fetch_ohlcv(self):
        since = self.db.newest_timestamp()
        # some exchanges use since as an exclusive limit
        # we ask again for the last candle in case the last time we
        # got that data, it was not closed yet and contained partial data
        if since is not None:
            since -= 1

            # we store timestamps in seconds, ccxt uses millis
            since = secs_to_millis(since)

        try:
            data = self.exchange.fetch_ohlcv(self.symbol, timeframe='1m', since=since)
            timestamps_to_seconds(data)
        except ccxt.NetworkError as err:
            print(f'ERROR: {err}')
            data = []

        return data


    def fetch_and_save(self):
        data = self.fetch_ohlcv()

        if len(data) > 0:
            self.db.add(data)

        for datum in data:
            date = datetime.fromtimestamp(datum[0]).strftime('%Y-%m-%d %H:%M:%S')
            print(date, datum)
        print()


    def run(self):
        print(f'sleep: {self.sleep_time}')

        while True:
            self.fetch_and_save()

            time.sleep(self.sleep_time)
