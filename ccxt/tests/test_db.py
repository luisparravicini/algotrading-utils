import pytest
from updater import Database


@pytest.fixture
def db(tmp_path):
    return Database(tmp_path.joinpath('db.db'))


def assert_rows(db, expected):
    count = db.conn.execute('SELECT COUNT(1) FROM ohlcv').fetchone()
    assert count == (expected, )


def test_create_empty(db):
    assert db.path.exists()


def test_creates_with_empty_table(db):
    assert_rows(db, 0)


def test_add(db):
    data = (1449999960,120.0000,119.0000,118.0000,117.0000,0.8000)
    db.add(data)
    assert_rows(db, 1)

    db_data = db.conn.execute('SELECT * FROM ohlcv').fetchone()
    assert db_data == data
