import ccxt


class MockExchange:
    VALID_SYMBOL = 'BTC/USD'
    VALID_NAME = 'kraken'
    INVALID_NAME = 'aabb'
    INVALID_SYMBOL = 'xxy/yzz'

    def __init__(self, exchange_name):
        self.exchange_name = exchange_name
        self.ohlcv_data = []
        self.test_fetch_ohlcv_error = None
    

    def fetch_ohlcv(self, symbol, timeframe, since):
        if symbol != MockExchange.VALID_SYMBOL:
            raise ccxt.BadSymbol()
        if self.test_fetch_ohlcv_error is not None:
            raise self.test_fetch_ohlcv_error
        
        self.test_since = since

        return self.ohlcv_data
