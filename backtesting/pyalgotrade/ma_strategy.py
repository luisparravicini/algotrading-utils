from __future__ import print_function

from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed, csvfeed
from pyalgotrade.technical import ma
from pyalgotrade.broker import backtesting


class MAStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, cash, fast_ma_time, slow_ma_time, take_profit_multiplier, stop_price_multiplier):
        # Create our broker defining the comission(0,01%)
        commission = backtesting.TradePercentage(0.0001)
        broker = backtesting.Broker(cash, feed, commission)

        super(MAStrategy, self).__init__(feed, broker)

        self.__fast_ma = ma.SMA(feed[instrument].getPriceDataSeries(), fast_ma_time)
        self.__slow_ma = ma.SMA(feed[instrument].getPriceDataSeries(), slow_ma_time)
        self.__instrument = instrument
        self.__takeProfitMultiplier = take_profit_multiplier
        self.__stopMultiplier = stop_price_multiplier

        self.__takeProfitPrice = None
        self.__stopPrice = None
        self.__position = None
        self.__lastTrend = None
        self.positions_taken = 0

    def getFastSMA(self):
        return self.__fast_ma

    def getSlowSMA(self):
        return self.__slow_ma

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self.__fast_ma[-1] is None or self.__slow_ma[-1] is None:
            return

        bar = bars[self.__instrument]
        if self.__position is None:
            self.open_position(bar)
        else:
            self.close_position(bar)

    def close_position(self, bar):
        """
            If we have an open position, we check if the asset price
            got to our take profit or stop loss price
        """

        exit_market = False
        shares = self.__position.getShares()

        if shares > 0:
            if bar.getPrice() > self.__takeProfitPrice or bar.getPrice() < self.__stopPrice:
                exit_market = True

        if shares < 0:
            if bar.getPrice() < self.__takeProfitPrice or bar.getPrice() > self.__stopPrice:
                exit_market = True

        if exit_market:
            self.__position.exitMarket()
            self.__position = None


    def open_position(self, bar):
        """
            If we don't have an open position, we check if there is an
            trend reversal
        """

        if self.__fast_ma[-1] > self.__slow_ma[-1] and self.__lastTrend != 'BULL':
            # If the trend is bullish, we buy 1 bitcoin and calculate the
            # take profit and stop loss prices
            self.__position = self.enterLong(self.__instrument, 1, True)
            self.__takeProfitPrice = bar.getPrice() * (1 + self.__takeProfitMultiplier)
            self.__stopPrice = bar.getPrice() * (1 - self.__stopMultiplier)
            self.__lastTrend = 'BULL'
            self.positions_taken += 1
            # self.debug(f'buying. instrument:${bar.getPrice()}, stop price:${self.__stopPrice:.2f}, take profit at:${self.__takeProfitPrice:.2f}')
            
        elif self.__fast_ma[-1] < self.__slow_ma[-1] and self.__lastTrend != 'BEAR':
            # If the trend is bearish, we sell 1 bitcoin and calculate the
            # take profit and stop loss prices
            self.__position = self.enterShort(self.__instrument, 1, True)
            self.__takeProfitPrice = bar.getPrice() * (1 - self.__takeProfitMultiplier)
            self.__stopPrice = bar.getPrice() * (1 + self.__stopMultiplier)
            self.__lastTrend = 'BEAR'
            self.positions_taken += 1
            # self.debug(f'selling. instrument:${bar.getPrice()}, stop price:${self.__stopPrice:.2f}, take profit at:${self.__takeProfitPrice:.2f}')
