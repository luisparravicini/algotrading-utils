import pytest
from updater import Filler
from mock_db import MockDB


@pytest.fixture
def filler(tmp_path):
    filler = Filler(tmp_path.joinpath('db.db'))
    filler.db = MockDB()
    return filler


def test_no_items(filler):
    filler.db.test_all_timestamps = list()
    assert filler.find_gaps() is None


def test_one_item(filler):
    filler.db.test_all_timestamps = [
        1449999961,
    ]
    gaps = filler.find_gaps()
    assert gaps.min == 1449999961
    assert gaps.max == 1449999961
    assert len(gaps.gaps) == 0


def test_two_items(filler):
    filler.db.test_all_timestamps = [
        1449999960,
        1449999961,
    ]
    gaps = filler.find_gaps()
    assert gaps.min == 1449999960
    assert gaps.max == 1449999961
    assert len(gaps.gaps) == 0

def test_no_gaps(filler):
    filler.db.test_all_timestamps = [
        1449999960,
        1449999961,
        1449999962,
    ]
    gaps = filler.find_gaps()
    assert gaps.min == 1449999960
    assert gaps.max == 1449999962
    assert [] == gaps.gaps

def test_one_gap(filler):
    filler.db.test_all_timestamps = [
        1449999960,
        1449999961,
        1449999964,
        1449999965,
    ]
    gaps = filler.find_gaps()
    assert gaps.min == 1449999960
    assert gaps.max == 1449999965
    assert [(1449999962, 1449999963)] == gaps.gaps


def test_several_gaps(filler):
    filler.db.test_all_timestamps = [
        1449999960,
        1449999961,
        1449999964,
        1449999968,
        1449999969,
    ]
    gaps = filler.find_gaps()
    assert gaps.min == 1449999960
    assert gaps.max == 1449999969
    assert [(1449999962, 1449999963), (1449999965, 1449999967)] == gaps.gaps


def test_gap_at_end(filler):
    filler.db.test_all_timestamps = [
        1449999960,
        1449999961,
        1449999964,
    ]
    gaps = filler.find_gaps()
    assert gaps.min == 1449999960
    assert gaps.max == 1449999964
    assert [(1449999962, 1449999963)] == gaps.gaps


def test_gap_at_beginning(filler):
    filler.db.test_all_timestamps = [
        1449999960,
        1449999964,
        1449999965,
    ]
    gaps = filler.find_gaps()
    assert gaps.min == 1449999960
    assert gaps.max == 1449999965
    assert [(1449999961, 1449999963)] == gaps.gaps
