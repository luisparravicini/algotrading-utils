import pytest
from updater import Database


@pytest.fixture
def db(tmp_path):
    return Database(tmp_path.joinpath('db.db'))


def assert_rows(db, expected):
    count = db.conn.execute('SELECT COUNT(1) FROM ohlcv').fetchone()
    assert count == (expected, )


def assert_one_row(db, expected):
    db_data = db.conn.execute('SELECT * FROM ohlcv').fetchone()
    assert db_data == expected


def test_create_empty(db):
    assert db.path.exists()


def test_creates_with_empty_table(db):
    assert_rows(db, 0)


def test_add(db):
    data = (1449999960,120.5000,119.6000,118.7000,117.8000,0.9000)
    db.add(data)
    assert_rows(db, 1)

    assert_one_row(db, data)


def test_add_update_with_same_timestamp(db):
    data1 = (1449999960,120,119,118,117,116)
    db.add(data1)
    data2 = (1449999960,999,999,999,999,999)
    db.add(data2)
    assert_rows(db, 1)

    assert_one_row(db, data2)
