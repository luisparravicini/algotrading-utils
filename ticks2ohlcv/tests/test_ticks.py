import ticks
import pytest
import io
from pathlib import Path


def build_path(dir, fname):
    return Path(__file__).parent.joinpath(dir, fname + '.csv')

def data_path(fname):
    return build_path('data', fname)

def data_expected_path(fname):
    return build_path('expected', fname)

def assert_result(data_fname, result):
    with open(data_expected_path(data_fname), 'r') as file:
        expected = file.read()

    output = result.to_csv(index=False)
    assert expected.split("\n") == output.split("\n")

def test_smoke_screen():
    data_fname = 'data_001'
    result = ticks.to_ohlcv(data_path(data_fname))
    
    assert_result(data_fname, result)
