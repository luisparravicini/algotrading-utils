import pytest
from updater import Updater
import ccxt
from copy import copy


class MockExchange:
    VALID_SYMBOL = 'BTC/USD'
    VALID_NAME = 'kraken'
    INVALID_NAME = 'aabb'
    INVALID_SYMBOL = 'xxy/yzz'

    def __init__(self, exchange_name):
        self.exchange_name = exchange_name
        self.ohlcv_data = []
    
    def fetch_ohlcv(self, symbol, timeframe, since):
        if symbol != MockExchange.VALID_SYMBOL:
            raise ccxt.BadSymbol()
        
        self.test_since = since

        return self.ohlcv_data


class MockDB:
    def __init__(self):
        self.test_data_add = None
        self.test_timestamp = None

    def add(self, data):
        self.test_data_add = data

    def newest_timestamp(self):
        return self.test_timestamp


@pytest.fixture
def updater(tmp_path):
    updater = Updater(MockExchange.VALID_NAME, MockExchange.VALID_SYMBOL, tmp_path)
    updater.exchange = MockExchange(updater.exchange.name)
    return updater


def test_unknown_exchange(tmp_path):
    name = MockExchange.INVALID_NAME
    assert name not in ccxt.exchanges

    with pytest.raises(AttributeError):
        Updater(name, MockExchange.VALID_SYMBOL, tmp_path)


def test_unknown_symbol(updater):
    updater.symbol = MockExchange.INVALID_SYMBOL
    with pytest.raises(ccxt.BadSymbol):
        updater.fetch_ohlcv()


def test_database_path(updater):
    assert updater.db is not None
    assert updater.db.path == updater.db_path


def test_database_name(updater):
    assert updater.db_path.name == 'kraken_btc_usd.db'


def test_database_inside_db_path(updater):
    assert updater.db_path.parent == updater.db_base_path


def test_fetch_ohlcv(updater):
    expected = [[11609370820000], [1609370830000], [1609370840000]]
    updater.exchange.ohlcv_data = copy(expected)
    assert updater.fetch_ohlcv() == expected


def test_fetch_ohlcv_empty(updater):
    updater.exchange.ohlcv_data = []
    assert updater.fetch_ohlcv() == []


def test_fetch_ohlcv_converts_to_secs(updater):
    updater.exchange.ohlcv_data = [
        [1609370820000, 9, 9, 9, 9, 9]
    ]
    assert updater.fetch_ohlcv() == [[1609370820, 9, 9, 9, 9, 9]]


def test_fetch_and_save(updater):
    updater.db = MockDB()
    updater.exchange.ohlcv_data = [
        [1609370820000, 9, 9, 9, 9, 9],
        [1609370820000, 8, 8, 8, 8, 8]
    ]
    updater.fetch_and_save()
    assert updater.db.test_data_add == [
        [1609370820, 9, 9, 9, 9, 9],
        [1609370820, 8, 8, 8, 8, 8]
    ]


def test_fetch_since_with_empty_db(updater):
    updater.db = MockDB()
    updater.fetch_ohlcv()
    assert updater.exchange.test_since == None


def test_fetch_since_with_data(updater):
    expected = 1609370820000
    updater.db = MockDB()
    updater.db.test_timestamp = expected // 1000 + 1
    
    updater.fetch_ohlcv()

    assert updater.exchange.test_since == expected
