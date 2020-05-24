import pytest

from argparse_custom_types import argparse_custom_types


@pytest.mark.parametrize("test_values, expected_results", [
    ("0", 0), ("1", 1), ("2", 2), ("3", 3), ("4", 4),
])
def test_int_range_value(test_values, expected_results):
    test_custom_type = argparse_custom_types.int_range(0, 5)
    result = test_custom_type(test_values)
    assert result == expected_results


@pytest.mark.parametrize("start, stop", [
    (0, 15), (5, 20), (0, 11),
    (10, 20), (-5, 20),
])
def test_int_range_start_stop(start, stop):
    test_value = "10"
    test_custom_type = argparse_custom_types.int_range(start, stop)
    result = test_custom_type(test_value)
    assert result == 10


@pytest.mark.parametrize("start, stop, step, value, expected", [
    (0, 15, 2, "4", 4),
    (5, 20, 5, "15", 15),
    (-10, 20, 2, "4", 4),
    (-10, 20, 2, "-4", -4),
    (0, -20, -2, "-8", -8),
])
def test_int_range_full(start, stop, step, value, expected):
    test_custom_type = argparse_custom_types.int_range(start, stop, step)
    result = test_custom_type(value)
    assert result == expected


@pytest.mark.parametrize("test_values", [
    "-5", "5", "600", "-20000", ""
])
def test_int_range_value_not_in_range(test_values, ):
    test_custom_type = argparse_custom_types.int_range(0, 5)
    with pytest.raises(argparse_custom_types.argparse.ArgumentTypeError):
        test_custom_type(test_values)


@pytest.mark.parametrize("test_values", [
    "A", "1.5", "string", "&&", "1+5", " ",
])
def test_int_range_fail(test_values):
    test_custom_type = argparse_custom_types.int_range(0, 5)
    with pytest.raises(argparse_custom_types.argparse.ArgumentTypeError):
        test_custom_type(test_values)


@pytest.mark.parametrize("start, stop, step", [
    (5, "30", None), (10.0, 20.0, None), (5, 30, 5.5),
    (5, "", ""), (5, None, None),
])
def test_int_range_setup_fail(start, stop, step):
    with pytest.raises(TypeError):
        argparse_custom_types.int_range(start, stop, step)

