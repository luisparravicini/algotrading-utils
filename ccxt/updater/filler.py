from pathlib import Path
from .db import Database
import collections


Gaps = collections.namedtuple('Gaps', ('min', 'max', 'gaps'))

class Filler:
    def __init__(self, db_path):
        self.db = Database(db_path)

    
    def find_gaps(self):
        min_tm = max_tm = None
        gaps = list()
        for timestamp in self.db.fetch_timestamps():
            max_tm = timestamp

            if min_tm is None:
                min_tm = timestamp
                last_tm = min_tm
                continue

            print((timestamp,last_tm), timestamp-last_tm,timestamp==last_tm)
            if timestamp - 1 != last_tm:
                gaps.append((last_tm + 1, timestamp - 1))
            
            last_tm = timestamp

        if min_tm is None:
            return None

        return Gaps(min_tm, max_tm, gaps)
