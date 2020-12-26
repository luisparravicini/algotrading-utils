# backtrader

The code is based on the code from [Getting started backtesting](https://analyzingalpha.com/backtrader-backtesting-trading-strategies)

## Requeriments

Install the dependencies with:

```
pip install --user -r requeriments.txt
```

Also, as of 2020-12-26, *backtrader* 1.9.76.123 has problems with the latest *matplotlib* (3.3.3) if you want to plot from *backtrader*. In my case, it worked installing an older *matplotlib* with:

```
pip uninstall matplotlib
pip install matplotlib==3.2.2
```

Also, you'll need *tkinter* for *matplotlib*, in Debian/Ubuntu systems install it with:

```
sudo apt-get install python3-tk
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
