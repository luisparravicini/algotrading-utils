import pytest
from updater import Filler
from mock_db import MockDB


@pytest.fixture
def filler(tmp_path):
    filler = Filler(tmp_path.joinpath('db.db'))
    filler.db = MockDB()
    return filler


def assert_gaps(min, max, gaps_data, filler):
    gaps = filler.find_gaps()
    assert gaps.min == min
    assert gaps.max == max
    assert gaps_data == gaps.gaps


def test_no_items(filler):
    filler.db.test_all_timestamps = list()
    assert filler.find_gaps() is None


def test_one_item(filler):
    filler.db.test_all_timestamps = [
        1449999961,
    ]
    assert_gaps(1449999961, 1449999961, list(), filler)


def test_two_items(filler):
    filler.db.test_all_timestamps = [
        1449999960,
        1449999961,
    ]
    assert_gaps(1449999960, 1449999961, list(), filler)


def test_no_gaps(filler):
    filler.db.test_all_timestamps = [
        1449999960,
        1449999961,
        1449999962,
    ]
    assert_gaps(1449999960, 1449999962, list(), filler)

def test_one_gap(filler):
    filler.db.test_all_timestamps = [
        1449999960,
        1449999961,
        1449999964,
        1449999965,
    ]
    assert_gaps(1449999960, 1449999965, [(1449999962, 1449999963)], filler)


def test_several_gaps(filler):
    filler.db.test_all_timestamps = [
        1449999960,
        1449999961,
        1449999964,
        1449999968,
        1449999969,
    ]
    assert_gaps(1449999960, 1449999969, [(1449999962, 1449999963), (1449999965, 1449999967)], filler)


def test_gap_at_end(filler):
    filler.db.test_all_timestamps = [
        1449999960,
        1449999961,
        1449999964,
    ]
    assert_gaps(1449999960, 1449999964, [(1449999962, 1449999963)], filler)


def test_gap_at_beginning(filler):
    filler.db.test_all_timestamps = [
        1449999960,
        1449999964,
        1449999965,
    ]
    assert_gaps(1449999960, 1449999965, [(1449999961, 1449999963)], filler)
