import pytest
from updater import Filler
from mock_db import MockDB


@pytest.fixture
def filler(tmp_path):
    filler = Filler(tmp_path.joinpath('db.db'))
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
        1449999961,
    ]
    assert_gaps(data, list(), filler)


def test_no_gaps(filler):
    data = [
        1449999960,
        1449999961,
        1449999962,
    ]
    assert_gaps(data, list(), filler)

def test_one_gap(filler):
    data = [
        1449999960,
        1449999961,
        1449999964,
        1449999965,
    ]
    assert_gaps(data, [(1449999962, 1449999963)], filler)


def test_several_gaps(filler):
    data = [
        1449999960,
        1449999961,
        1449999964,
        1449999968,
        1449999969,
    ]
    assert_gaps(data, [(1449999962, 1449999963), (1449999965, 1449999967)], filler)


def test_gap_at_end(filler):
    data = [
        1449999960,
        1449999961,
        1449999964,
    ]
    assert_gaps(data, [(1449999962, 1449999963)], filler)


def test_gap_at_beginning(filler):
    data = [
        1449999960,
        1449999964,
        1449999965,
    ]
    assert_gaps(data, [(1449999961, 1449999963)], filler)
