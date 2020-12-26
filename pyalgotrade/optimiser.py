import itertools
from pyalgotrade.optimizer import local
from ma_strategy import MAStrategy
from pyalgotrade.bar import Frequency
from pyalgotrade.barfeed import csvfeed
from pyalgotrade.broker import backtesting

def parameters_generator():
    instrument = ['BTC']
    initial_cash = [100000]
    take_profit_price = [f / 1000 for f in range(0, 1000)][:100]
    stop_price = [f / 1000 for f in range(0, 50)]
    fast_ma_time = range(2, 20)
    slow_ma_time = range(20, 120)

    # hardcoding these values, testing optimizing the ma slow/fast times
    take_profit_price = [0.0018]
    stop_price =[0.003]
    
    return itertools.product(instrument, initial_cash,
                             fast_ma_time, slow_ma_time,
                             take_profit_price, stop_price)

def main():
    instrument = 'BTC'
    frequency = Frequency.MINUTE
    feed = csvfeed.GenericBarFeed(frequency=frequency)
    feed.addBarsFromCSV(instrument, "sampledata.csv")

    local.run(MAStrategy, feed, parameters_generator())


if __name__ == '__main__':
    main()
