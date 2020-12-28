import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.joinpath('..').absolute()))

import ticks


if len(sys.argv) < 4:
    print(f'usage: {sys.argv[0]} <data_in_path> <interval> <data_out_path>')
    sys.exit(1)

data_in_path = sys.argv[1]
interval = int(sys.argv[2])
data_out_path = sys.argv[3]

print(f'parsing {data_in_path} in {interval}m frames')
df = ticks.to_ohlcv(data_in_path, interval)
ticks.export_dataframe(df, data_out_path)
print(f'exported parsed data to {data_out_path}')
