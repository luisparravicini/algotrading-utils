import backtrader as bt
from pathlib import Path
import pandas as pd

class SMACross(bt.SignalStrategy):
    def __init__(self):
        sma_short = bt.ind.SMA(period=5)
        sma_long = bt.ind.SMA(period=60)
        crossover = bt.ind.CrossOver(sma_short, sma_long)
        self.signal_add(bt.SIGNAL_LONG, crossover)


if __name__ == '__main__':
    data_path = Path(__file__).parent.joinpath('../pyalgotrade/sampledata.csv')
    dataframe = pd.read_csv(data_path,
                            parse_dates=True,
                            index_col=0)
    data = bt.feeds.PandasData(dataname=dataframe)

    cerebro = bt.Cerebro()
    initial_cash = 100000
    cerebro.broker.setcash(initial_cash)
    cerebro.addstrategy(SMACross)
    cerebro.adddata(data)

    print('Initial portfolio value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    result = cerebro.broker.getvalue()
    print('Final portfolio value: %.2f' % result)
    profit = result / float(initial_cash)
    print(f'profit: {profit:.3f}%')

    cerebro.plot()
