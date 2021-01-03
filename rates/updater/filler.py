from .db import Database
import collections
from .exchange import build_exchange, timestamps_to_seconds, secs_to_millis


Gaps = collections.namedtuple('Gaps', ('min', 'max', 'gaps'))

class Filler:
    def __init__(self, exchange_name, symbol, base_db_path):
        self.db = Database(exchange_name, symbol, base_db_path)
        self.exchange = build_exchange(exchange_name)
        self.symbol = symbol
    
    def find_gaps(self):
        interval = 60
        clear_secs = lambda x: (x // interval) * interval
        min_tm = max_tm = None
        gaps = list()
        for timestamp in self.db.fetch_timestamps():
            max_tm = timestamp

            if min_tm is None:
                min_tm = timestamp
                last_tm = clear_secs(min_tm)
                continue

            timestamp = clear_secs(timestamp)
            if timestamp != last_tm and timestamp - interval != last_tm:
                gaps.append((last_tm + interval, timestamp - interval))
            
            last_tm = timestamp

        if min_tm is None:
            return None

        return Gaps(min_tm, max_tm, gaps)


    def fill(self, start_timestamp, stop_timestamp, verbose=False):
        start_timestamp = secs_to_millis(start_timestamp)
        stop_timestamp = secs_to_millis(stop_timestamp)

        since = start_timestamp
        while since < stop_timestamp:
            if verbose:
                print(f'fetching since {since}', end='', flush=True)

            data = self.exchange.fetch_ohlcv(self.symbol, timeframe='1m', since=since)
            since = max(data, key=lambda x: x[0])[0]

            data_in_range = list(filter(lambda x: x[0] <= stop_timestamp, data))
            print(data)
            print(stop_timestamp)

            timestamps_to_seconds(data_in_range)
            self.db.add(data_in_range)

            if verbose:
                print(f', got {len(data_in_range)}')
