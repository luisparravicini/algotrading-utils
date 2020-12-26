# backtrader

The code is based on the code from [Getting started backtesting](https://analyzingalpha.com/backtrader-backtesting-trading-strategies)

## Requeriments

Install the dependencies with:

```
pip install --user -r requeriments.txt
```

As of 2020-12-26, *backtrader* 1.9.76.123 has problems with the latest *matplotlib* (3.3.3) if you want to plot from *backtrader*. In my case, it worked installing an older version:

```
pip uninstall matplotlib
pip install matplotlib==3.2.2
```

You'll also need *tkinter* (used by *matplotlib*), in Debian/Ubuntu systems install it with:

```
sudo apt-get install python3-tk
```

I use the same data collected by the *pyalgotrade* example. Check out the [README](../pyalgotrade/README.md) on how to run it.

## Backesting

Run

```
python strategy.py
```

After it runs it will print the returns and open a *matplotlib* graph.
