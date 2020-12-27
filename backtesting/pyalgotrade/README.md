# pyalgotrade

The code is based on [https://github.com/8ball030/ftx_competition_entry](ftx_competition_entry) and [https://github.com/andreHashimoto/trading-strategy-backtest](trading-strategy-backtest).


## Requeriments

Install the dependencies with:

```
pip install --user -r requeriments.txt
```

The data needed to test the strategy can be downloaded with `data_gather.py`. It will try to download a whole day of data in 1 minute intervals. Sometimes depending on the exchage, the data returned will be less than one day.

## Backesting

Run

```
python strategy.py
```

After it runs it will print the returns and open a *matplotlib* graph.


## Optimisation

To optimise the strategy, run:


```
python3 optimiser.py

```

What it basically does is: you give *pylagotrade* lists of different options for configuring the strategy and it tests them all, printing the best combinations found.
