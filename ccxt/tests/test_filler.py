import pytest
from updater import Filler
from mock_db import MockDB


@pytest.fixture
def filler(tmp_path):
    filler = Filler('kraken', 'BTC/USD', tmp_path)
    filler.db = MockDB()
    return filler


def assert_gaps(data, gaps_data, filler):
    filler.db.test_all_timestamps = data
    gaps = filler.find_gaps()
    assert gaps.min == min(data)
    assert gaps.max == max(data)
    assert gaps_data == gaps.gaps


def test_no_items(filler):
    filler.db.test_all_timestamps = list()
    assert filler.find_gaps() is None


def test_one_item(filler):
    data = [
        1449999961,
    ]
    assert_gaps(data, list(), filler)


def test_two_items(filler):
    data = [
        1449999960,
        1450000020,
    ]
    assert_gaps(data, list(), filler)


def test_no_gaps_all_in_same_minute(filler):
    data = [
        1449999960,
        1449999961,
        1449999962,
    ]
    assert_gaps(data, list(), filler)


def test_no_gaps(filler):
    data = [
        1449999960,
        1450000020,
        1450000080,
    ]
    assert_gaps(data, list(), filler)

def test_one_gap_of_one_min(filler):
    data = [
        1449999960,
        1450000020,
        1450000140,
        1450000200,
    ]
    assert_gaps(data, [(1450000080, 1450000080)], filler)

def test_one_gap_bigger_than_1m(filler):
    data = [
        1449999960,
        1450000020,
        1450000200,
        1450000260,
    ]
    assert_gaps(data, [(1450000080, 1450000140)], filler)


def test_several_gaps(filler):
    data = [
        1449999960,
        1450000020,
        1450000200,
        1450000320,
        1450000380,
    ]
    assert_gaps(data, [(1450000080, 1450000140), (1450000260, 1450000260)], filler)


def test_gap_at_end(filler):
    data = [
        1449999960,
        1450000020,
        1450000140,
    ]
    assert_gaps(data, [(1450000080, 1450000080)], filler)


def test_gap_at_beginning(filler):
    data = [
        1449999960,
        1450000140,
        1450000200,
    ]
    assert_gaps(data, [(1450000020, 1450000080)], filler)
