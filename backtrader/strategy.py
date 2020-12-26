import backtrader as bt
from pathlib import Path
import pandas as pd

class SMACross(bt.SignalStrategy):
    def __init__(self):
        sma_short = bt.ind.SMA(period=10)
        sma_long = bt.ind.SMA(period=20)
        crossover = bt.ind.CrossOver(sma_short, sma_long)
        self.signal_add(bt.SIGNAL_LONG, crossover)


if __name__ == '__main__':
    data_path = Path(__file__).parent.joinpath('../pyalgotrade/sampledata.csv')
    dataframe = pd.read_csv(data_path,
                            parse_dates=True,
                            index_col=0)
    data = bt.feeds.PandasData(dataname=dataframe)

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000)
    cerebro.addstrategy(SMACross)
    cerebro.adddata(data)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()
