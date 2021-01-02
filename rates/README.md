## ccxt

Here are some tests I've made using ccxt, everything here is a WIP.

Currently there's code to connect to an exchange, pull the ohlcv data periodically and save it to a SQLite3 database.


## Requeriments

Install the production and development dependencies with `make install-deps`

## Run it

You can the script with `bin/updater.sh`. It needs three parameters: *exchange name*, *symbol* and path to where the database will be created. The path needs to exist.

```
./bin/updater.sh kraken BTC/USD ./data
```

## Docker

There's a Dockerfile to run the script dockerized. It can be run with `make docker-run`. It will build the image first if it doesn't exist.

The path where the script creates the database is mounted on the host in the `data` directory created before running docker.
