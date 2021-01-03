## rate updater

Rate updater lets you periodically poll an exchange's pair rate and save it to a SQLite3 database.
It can also fetch older data on demand.

**NOTE**: Since I wrote this, I've found [guptarohit/cryptoCMD](https://github.com/guptarohit/cryptoCMD) which seems to do something similar and looks more mature than what I wrote. Haven't used *cryptoCMD* yet, though.


## Requeriments

Install the production and development dependencies with `make install-deps`

## Updater

You can the script with `bin/updater.sh`. It needs three parameters: *exchange name*, *symbol* and path to where the database will be created. The path needs to exist.

```
./bin/updater.sh kraken BTC/USD ./data
```

## Gaps

You can check if there are missing info in the downloaded data with:

```
python -m updater.main gaps <exchange> <pair> <data_path>
```

It will list the min/max date found and a list of gaps found:

```
min: 2020-12-31T03:47:00 (1609397220)
max: 2021-01-03T08:44:00 (1609674240)
gaps:
  (2021-01-01T19:40:00 - 2021-01-01T21:14:00, 94m) (1609540800-1609546440)
  (2021-01-02T15:44:00 - 2021-01-02T20:29:00, 285m) (1609613040-1609630140)
```


## Docker

There's a Dockerfile to run the script dockerized. It can be run with `make docker-run`. It will build the image first if it doesn't exist.

The path where the script creates the database is mounted on the host in the `data` directory created before running docker.


## Tests

Tests can be run with `make tests`
