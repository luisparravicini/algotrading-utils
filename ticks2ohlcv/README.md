# ticks to OHLCV

Converts tick data to OHLCV data in a specified time interval (defaults to 1m).

The input data needs to be csv with three columns: *timestamp* in UTC, *price* and *volume*. Something like this:

```csv
1449999960,120.00000,0.50000000
```

Run it with:

```
python bin/to_ohlcv.py <data_in_path> <time_interval_in_minutes> <data_out_path>
```

The parsed csv looks like this:

```csv
date,open,high,low,close,volume
1449999960,120.0000,120.0000,120.0000,120.0000,0.0000
```
