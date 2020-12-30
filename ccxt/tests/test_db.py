import pytest
from updater import Database


@pytest.fixture
def db(tmp_path):
    return Database(tmp_path.joinpath('db.db'))


def test_create_empty(db):
    assert db.path.exists()

def test_creates_with_empty_table(db):
    count = db.conn.execute('SELECT COUNT(1) FROM ohlcv').fetchone()
    assert count == (0, )