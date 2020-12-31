## ccxt

Here are some tests I've made using ccxt, everything here is a WIP.

Currently there's code to connect to an exchange, pull the ohlcv data periodically and save it to a SQLite3 database.


## Requeriments

Install the dependencies with:

```
pip install --user -r requeriments.txt
```

And the dev dependencies are listed in `requeriments-dev.txt`


## Run it

You can the script with `bin/updater.sh`. It needs three parameters: *exchange name*, *symbol* and path to where the database will be created.

```
./bin/updater.sh kraken BTC/USD ./data
```

## Docker

There's a Dockerfile to run the script dockerized. The image can be build with:

```
docker -t updater build .
```

And you can the container with:

```
mkdir data
docker run -it --mount type=bind,source="$(pwd)"/data,target=/app/data updater
```

The path where the script creates the database is mount on the host in the `data` directory created before running docker.
