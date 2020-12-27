import ticks
import pytest
import io
from pathlib import Path

def data_path(fname):
    return Path(__file__).parent.joinpath('data', fname + '.csv')

def data_expected_path(fname):
    return Path(__file__).parent.joinpath('expected', fname + '.csv')

def assert_result(data_fname, result):
    with open(data_expected_path(data_fname), 'r') as file:
        expected = file.read()

    output = result.to_csv(index=False)
    assert expected.split("\n") == output.split("\n")

def test_1m():
    data_fname = 'data_001'

    # result = io.StringIO()
    with open(data_path(data_fname), 'r') as fd_in:
        result = ticks.to_ohlcv(fd_in, None)
    
    assert_result(data_fname, result)
