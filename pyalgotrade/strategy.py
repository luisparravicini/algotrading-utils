from pyalgotrade import strategy
from pyalgotrade.bar import Frequency
from pyalgotrade.barfeed import csvfeed
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import trades

from pyalgotrade import plotter

from ma_strategy import MAStrategy

def run_strategy(fast_ma_time, slow_ma_time,
                 take_profit_price, stop_price):
    instrument = 'BTC'
    frequency = Frequency.MINUTE
    feed = csvfeed.GenericBarFeed(frequency=frequency)
    feed.addBarsFromCSV(instrument, "sampledata.csv")

    initial_cash = 100000
    strategy = MAStrategy(feed, instrument, initial_cash,
                             fast_ma_time, slow_ma_time,
                             take_profit_price, stop_price)

    returnsAnalyzer = returns.Returns()
    strategy.attachAnalyzer(returnsAnalyzer)
    tradesAnalyzer = trades.Trades()
    strategy.attachAnalyzer(tradesAnalyzer)

    plt = plotter.StrategyPlotter(strategy)
    plt.getOrCreateSubplot("MA").addDataSeries(f'{fast_ma_time} MA', strategy.getFastSMA())
    plt.getOrCreateSubplot("MA").addDataSeries(f'{slow_ma_time} MA', strategy.getSlowSMA())

    plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())

    strategy.info(f'Initial portfolio value: ${initial_cash:.2f}')
    strategy.run()
    result = strategy.getResult()
    profit = result / float(initial_cash)
    strategy.info(f'Final portfolio value: ${result:.2f}')
    strategy.info(f'profit: {profit:.3f}%')
    strategy.info(f'positions taken: {strategy.positions_taken}')

    plt.plot()


if __name__ == "__main__":
    take_profit = 0.018
    stop_price = 0.003
    fast_ma_time = 10
    slow_ma_time = 80
    run_strategy(fast_ma_time, slow_ma_time, take_profit, stop_price)
