import sys
from datetime import datetime
from updater import Updater, Filler


def updater_main(exchange_name, symbol, db_path):
    print(f'starting updater for {exchange_name}:{symbol}')
    print(f'data path: {db_path}')
    updater = Updater(exchange_name, symbol, db_path)
    updater.run()


def filler_main(exchange_name, symbol, db_path):
    filler = Filler(exchange_name, symbol, db_path)

    def iso8601(timestmap_secs):
        return datetime.fromtimestamp(timestmap_secs).isoformat()

    gaps = filler.find_gaps()
    print(f'min: {iso8601(gaps.min)} ({gaps.min})')
    print(f'max: {iso8601(gaps.max)} ({gaps.max})')
    print('gaps:')
    for gap in gaps.gaps:
        print(f'  ({iso8601(gap[0])} - {iso8601(gap[1])}) ({gap[0]}-{gap[1]})')


action = sys.argv[1]
exchange_name = sys.argv[2]
symbol = sys.argv[3]
db_path = sys.argv[4]

if action == 'updater':
    updater_main(exchange_name, symbol, db_path)
elif action =='filler':
    filler_main(exchange_name, symbol, db_path)
