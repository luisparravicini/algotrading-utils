# ticks to OHLCV

Converts tick data to OHLCV data in a specified time interval.

The input data needs to be in csv format with three columns: *timestamp* in UTC, *price* and *volume*.

```csv
1449999960,120.00000,0.50000000
```

Run the script with:

```
python bin/to_ohlcv.py <data_in_path> <time_interval_in_minutes> <data_out_path>
```

The parsed csv looks like this:

```csv
date,open,high,low,close,volume
2015-12-13 06:45:00,120.0000,120.0000,120.0000,120.0000,0.0000
```
