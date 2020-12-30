import pytest
from updater import Updater
import ccxt


class MockExchange:
    VALID_SYMBOL = 'BTC/USD'
    VALID_NAME = 'kraken'
    INVALID_NAME = 'aabb'
    INVALID_SYMBOL = 'xxy/yzz'

    def __init__(self, exchange_name):
        self.exchange_name = exchange_name
    
    def fetch_ohlcv(self, symbol, timeframe, limit):
        raise ccxt.BadSymbol()

@pytest.fixture
def exchange(tmp_path):
    return Updater(MockExchange.VALID_NAME, MockExchange.VALID_SYMBOL, tmp_path)


def test_unknown_exchange(tmp_path):
    name = MockExchange.INVALID_NAME
    assert name not in ccxt.exchanges

    with pytest.raises(AttributeError):
        Updater(name, MockExchange.VALID_SYMBOL, tmp_path)


def test_unknown_symbol(tmp_path):
    updater = Updater('kraken', MockExchange.INVALID_SYMBOL, tmp_path)
    updater.exchange = MockExchange(updater.exchange.name)
    with pytest.raises(ccxt.BadSymbol):
        updater.fetch_ohlcv()


def test_create_database(exchange):
    assert exchange.db_path.exists()

def test_database_name_is_exchange(exchange):
    assert exchange.db_path.name == exchange.exchange_name + '.db'
