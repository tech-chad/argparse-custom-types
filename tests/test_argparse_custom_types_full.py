import argparse
import pytest

from argparse_custom_types import argparse_custom_types


def _argparse_runner(test_type, test_values):
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", dest="test_type", type=test_type)
    args = parser.parse_args(["-t", str(test_values)])
    return args.test_type


def _argparse_runner_raises(test_type, test_values):
    with pytest.raises(SystemExit):
        _argparse_runner(test_type, test_values)


@pytest.mark.parametrize("start_stop_step, test_values, expected_results", [
    ((5, 20), "10", 10), ((-20, -5), "-10", -10),
    ((5, 20, 5), "15", 15), ((0, -20, -2), "-12", -12)
])
def test_int_range_full(start_stop_step, test_values, expected_results):
    test_type = argparse_custom_types.int_range(*start_stop_step)
    result = _argparse_runner(test_type, test_values)
    assert result == expected_results


@pytest.mark.parametrize("start_stop_step, test_values", [
    ((5, 20), "10.5"), ((5, 20), "string"), ((5, 20), "5g"),
    ((5, 20), "20"), ((5, 20), "-10"), ((2, 21, 2), "7"),
])
def test_int_range_full_fail(start_stop_step, test_values, capsys):
    start = start_stop_step[0]
    stop = start_stop_step[1]
    test_type = argparse_custom_types.int_range(*start_stop_step)
    _argparse_runner_raises(test_type, test_values)
    captured = capsys.readouterr().err
    assert f"{test_values} is an invalid int value in " \
           f"range {start} - {stop}" in captured
