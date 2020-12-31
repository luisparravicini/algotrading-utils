import sys
from updater import Updater


exchange_name = sys.argv[1]
symbol = sys.argv[2]
db_path = sys.argv[3]

print(f'starting updater for {exchange_name}:{symbol}')
print(f'data path: {db_path}')
updater = Updater(exchange_name, symbol, db_path)
updater.run()
