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


@pytest.mark.parametrize("min_value, test_values, expected_results", [
    (5, "5", 5), (5, "6", 6), (-500, "-350", -350)
])
def test_int_above_full(min_value, test_values, expected_results):
    test_type = argparse_custom_types.int_above(min_value)
    result = _argparse_runner(test_type, test_values)
    assert result == expected_results


@pytest.mark.parametrize("min_value, test_value", [
    (40, "39"), (40, "-39"), (-35, "-45"),
    (5, "string"), (5, "10.5"), (5, "=10"),
])
def test_int_above_full_fail(min_value, test_value, capsys):
    test_type = argparse_custom_types.int_above(min_value)
    _argparse_runner_raises(test_type, test_value)
    captured = capsys.readouterr().err
    assert f"{test_value} is an invalid int value above {min_value}" in captured


@pytest.mark.parametrize("max_value, test_value, expected_result", [
    (10, "5", 5), (-10, "-20", -20), (50, "-120", -120)
])
def test_int_below_full(max_value, test_value, expected_result):
    test_type = argparse_custom_types.int_below(max_value)
    result = _argparse_runner(test_type, test_value)
    assert result == expected_result


@pytest.mark.parametrize("max_value, test_value", [
    (10, "12"), (-10, "-9"), (20, "string"), (20, "10.8"),
])
def test_int_below_full_fail(max_value, test_value, capsys):
    test_type = argparse_custom_types.int_below(max_value)
    _argparse_runner_raises(test_type, test_value)
    captured = capsys.readouterr().err
    assert f"{test_value} is an invalid int value below {max_value}" in captured


@pytest.mark.parametrize("test_seq, test_value", [
    (["1", "string", "0.45%"], "1"),
    (("1", "string", "0.45%"), "string"),
    (["1", "string", "0.45%"], "0.45%"),
])
def test_in_sequence_string_full(test_value, test_seq):
    test_type = argparse_custom_types.in_sequence_strings(test_seq)
    result = _argparse_runner(test_type, test_value)
    assert result == test_value


@pytest.mark.parametrize("test_seq, test_value", [
    (("50", "test", "$4.45"), "5"),
    (["50", "test", "$4.45"], "string"),
])
def test_in_sequence_string_full_fail(test_seq, test_value, capsys):
    test_type = argparse_custom_types.in_sequence_strings(test_seq)
    _argparse_runner_raises(test_type, test_value)
    captured = capsys.readouterr().err
    assert f"{test_value} is not in the excepted value list" in captured


@pytest.mark.parametrize("test_seq", [
    ["a", "string", "1", "$4.50"],
    ("a", "string", "1", "$4.50")
])
def test_in_sequence_string_full_fail_show(test_seq, capsys):
    test_type = argparse_custom_types.in_sequence_strings(test_seq, True)
    _argparse_runner_raises(test_type, "20")
    captured = capsys.readouterr().err
    assert f"""20 is not in the excepted value list
a, string, 1, $4.50""" in captured
