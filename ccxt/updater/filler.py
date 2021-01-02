from .db import Database
import collections


Gaps = collections.namedtuple('Gaps', ('min', 'max', 'gaps'))

class Filler:
    def __init__(self, exchange_name, symbol, base_db_path):
        self.db = Database(exchange_name, symbol, base_db_path)

    
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
