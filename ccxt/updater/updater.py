from datetime import datetime
import ccxt
import time
from pathlib import Path


class Updater:
    def __init__(self, exchange_name, symbol, db_base_path):
        self.exchange_name = exchange_name
        exchange = getattr(ccxt, exchange_name)
        self.exchange = exchange({
            'enableRateLimit': True
        })

        self.symbol = symbol

        self.db_base_path = db_base_path
        # exchange_name should be composed of only alphanumeric chars!
        self.db_path = Path(self.db_base_path).joinpath(exchange_name + '.db')
        self.db_path.touch()

    def run(self):
        pass

    def fetch_ohlcv(self):
        return self.exchange.fetch_ohlcv(self.symbol, timeframe='1m', limit=20)

# while True:
#     # limit=20, why?
#     #
#     # The list item will be discarded and the rest are just in case
#     # the updater crashes and some time passes before the updater starts
#     # again
#     data = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=20)

#     # data = [[1609237560000, 26752.5, 26752.5, 26736.7, 26736.7, 0.3], [1609237620000, 26746.6, 26752.6, 26746.6, 26752.6, 5.10782857], [1609237680000, 26752.6, 26757.1, 26752.6, 26757.1, 2.98049269], [1609237740000, 26758.3, 26797.5, 26758.3, 26797.5, 0.52433178], [1609237800000, 26797.4, 26817.7, 26792.0, 26797.4, 18.71965105], [1609237860000, 26797.4, 26797.4, 26797.4, 26797.4, 1.003698], [1609237920000, 26791.6, 26791.6, 26790.0, 26790.0, 0.84944304], [1609237980000, 26759.3, 26759.3, 26752.7, 26752.7, 7.97442654], [1609238040000, 26752.8, 26752.8, 26721.3, 26721.3, 2.57895496], [1609238100000, 26729.6, 26729.6, 26686.1, 26694.6, 3.23059703]]

#     # according to ccxt docs:
#     #
#     # "Note that the info from the last (current) candle may be incomplete until
#     # the candle is closed (until the next candle starts)."
#     #
#     # so the last item is discarded
#     data = data[:-1]

#     for datum in data:
#         date = datetime.fromtimestamp(datum[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
#         print(date, datum)


#     time.sleep(45)
