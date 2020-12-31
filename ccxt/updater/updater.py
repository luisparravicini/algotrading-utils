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
        # limit=20, why?
        #
        # The list item will be discarded and the rest are just in case
        # the updater crashes and some time passes before the updater starts
        # again
        data = self.exchange.fetch_ohlcv(self.symbol, timeframe='1m', limit=20)

        # according to ccxt docs:
        #
        # "Note that the info from the last (current) candle may be incomplete until
        # the candle is closed (until the next candle starts)."
        #
        # so the last item is discarded
        data = data[:-1]

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
