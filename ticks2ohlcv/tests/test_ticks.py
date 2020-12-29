import ticks
import pytest
import io
from pathlib import Path
import tempfile


def build_path(dir, fname):
    return Path(__file__).parent.joinpath(dir, fname + '.csv')

def data_path(fname):
    return build_path('data', fname)

def data_expected_path(fname):
    return build_path('expected', fname)

def assert_conversion(data_fname, interval=1):
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_path = Path(tmp_dir, 'out.csv')
        ticks.to_ohlcv(data_path(data_fname), out_path, interval)
        
        assert out_path.exists()
        with open(out_path, 'r') as file:
            ohlcv_data = file.read()

    with open(data_expected_path(data_fname), 'r') as file:
        expected = file.read()

    assert expected.split("\n") == ohlcv_data.split("\n")

def test_reset_seconds():
    assert_conversion('data_001')

def test_min():
    assert_conversion('data_002')

def test_rows_in_an_interval_are_collapsed():
    assert_conversion('data_003')

def test_max():
    assert_conversion('data_004')

def test_open():
    assert_conversion('data_005')

def test_close():
    assert_conversion('data_006')

def test_5m_interval():
    assert_conversion('data_007', interval=5)

def test_volume():
    assert_conversion('data_008')

def test_output_last_frame():
    assert_conversion('data_009')
