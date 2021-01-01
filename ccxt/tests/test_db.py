import pytest
from updater import Database
import sqlite3


@pytest.fixture
def db(tmp_path):
    return Database(tmp_path.joinpath('db.db'))


def db_exec(db_path, query):
    with sqlite3.connect(db_path) as conn:
        yield conn.execute(query)


def assert_row_count(db, expected):
    count = next(db_exec(db.path, 'SELECT COUNT(1) FROM ohlcv')).fetchone()
    assert count == (expected, )


def assert_rows_data(db, expected):
    db_data = next(db_exec(db.path, 'SELECT * FROM ohlcv')).fetchall()
    assert db_data == expected


def test_create_empty(db):
    assert db.path.exists()


def test_creates_with_empty_table(db):
    assert_row_count(db, 0)


def test_add(db):
    data = (1449999960,120.5000,119.6000,118.7000,117.8000,0.9000)
    db.add([data])

    assert_rows_data(db, [data])


def test_add_several(db):
    data1 = (1449999960,120,119,118,117,116)
    db.add([data1])
    data2 = (1449999961,999,999,999,999,999)
    db.add([data2])

    assert_rows_data(db, [data1, data2])


def test_add_update_with_same_timestamp(db):
    data1 = (1449999960,120,119,118,117,116)
    db.add([data1])
    data2 = (1449999960,999,999,999,999,999)
    db.add([data2])

    assert_rows_data(db, [data2])


def test_newest_timestamp_when_empty(db):
    assert db.newest_timestamp() is None


def test_newest_timestamp(db):
    expected = 2549999960
    db.add([
        (1449999960,120,119,118,117,116),
        (expected,999,999,999,999,999),
        (1449999980,999,999,999,999,999)
    ])

    assert db.newest_timestamp() == expected


def test_fetch_timestamps_several(db):
    db.add([
        (1449999960,120,119,118,117,116),
        (1449999980,999,999,999,999,999)
    ])

    assert [1449999960, 1449999980] == list(db.fetch_timestamps())


def test_fetch_timestamps_empty(db):
    print(list(db.fetch_timestamps()))
    assert [] == list(db.fetch_timestamps())


def test_fetch_timestamps_ordered(db):
    db.add([
        (1449999980,999,999,999,999,999),
        (1449999960,120,119,118,117,116)
    ])

    assert [1449999960, 1449999980] == list(db.fetch_timestamps())
