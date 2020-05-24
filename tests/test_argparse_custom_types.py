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


@pytest.mark.parametrize("min_value, test_value, expected_result", [
    (20, "20", 20), (20, "21", 21), (500, "20000", 20000),
    (0, "0", 0), (-50, "-20", -20), (-50, "0", 0), (-50, "20", 20),
    (10.5, "12", 12),
])
def test_int_above(min_value, test_value, expected_result):
    test_type = argparse_custom_types.int_above(min_value)
    result = test_type(test_value)
    assert result == expected_result


@pytest.mark.parametrize("min_value, test_value", [
    (20, "19"), (20, "0"), (20, "-20"),
    (-20, "-21"), (-20, "-400"), (10.5, "10"),
    (10, "12.5"), (10.5, "12.5"),
])
def test_int_above_fail(min_value, test_value):
    test_type = argparse_custom_types.int_above(min_value)
    with pytest.raises(argparse_custom_types.argparse.ArgumentTypeError):
        test_type(test_value)


@pytest.mark.parametrize("max_value, test_value, expected_result", [
    (20, "15", 15), (20, "-10", -10), (0, "0", 0),
    (-10, "-25", -25)
])
def test_int_below(max_value, test_value, expected_result):
    test_type = argparse_custom_types.int_below(max_value)
    result = test_type(test_value)
    assert result == expected_result


@pytest.mark.parametrize("max_value, test_value", [
    (20, "21"), (15, "215"), (-25, "-19"),
    (20, "string"), (20, "10.4"),
])
def test_int_below_fail(max_value, test_value):
    test_type = argparse_custom_types.int_below(max_value)
    with pytest.raises(argparse_custom_types.argparse.ArgumentTypeError):
        test_type(test_value)


@pytest.mark.parametrize("test_seq, test_value", [
    (["1", "4", "7", "10"], "7"),
    (("3", "7", "10", "12"), "12"),
    (["one", "two", "three"], "one"),
    (("test", "100", "10.5", "$6.00"), "$6.00"),
    (("test", "100", "10.5", "$6.00"), "10.5"),
])
def test_in_sequence_string(test_seq, test_value):
    test_type = argparse_custom_types.in_sequence_strings(test_seq)
    result = test_type(test_value)
    assert result == test_value


@pytest.mark.parametrize("test_seq, test_value", [
    (["1", "five", "8.89", "*90"], "5"),
    (["1", "five", "8.89", "*90"], "8"),
    (["1", "five", "8.89", "*90"], "string"),
    (("1", "five", "8.89", "*90"), "1.0"),
])
def test_in_sequence_string(test_seq, test_value):
    test_type = argparse_custom_types.in_sequence_strings(test_seq)
    with pytest.raises(argparse_custom_types.argparse.ArgumentTypeError):
        test_type(test_value)


@pytest.mark.parametrize("test_value, expected_result", [
    ("2", 2), ("12", 12), ("48", 48), ("345992", 345992),
])
def test_int_even_default(test_value, expected_result):
    test_type = argparse_custom_types.int_even()
    result = test_type(test_value)
    assert result == expected_result


@pytest.mark.parametrize("options, test_values, expected_result", [
    ((True, True, False), "10", 10),
    ((True, True, False), "-10", -10),
    ((True, True, False), "-122", -122),
    ((True, True, True), "0", 0),
    ((False, True, False), "-22", -22),
    ((False, True, True), "0", 0),
])
def test_int_even_options(options, test_values, expected_result):
    test_type = argparse_custom_types.int_even(*options)
    result = test_type(test_values)
    assert result == expected_result


@pytest.mark.parametrize("options, test_value", [
    ((True, False, False), "0"),
    ((True, False, False), "-22"),
    ((True, False, False), "99"),
    ((True, True, False), "0"),
    ((True, True, False), "-87"),
    ((False, True, False), "22"),
    ((False, True, False), "-23"),
    ((False, True, False), "0"),
])
def test_int_even_options_fail(options, test_value):
    test_type = argparse_custom_types.int_even(*options)
    with pytest.raises(argparse_custom_types.argparse.ArgumentTypeError):
        test_type(test_value)


@pytest.mark.parametrize("options, test_value, expected_results", [
    ((True, False, False), "5", 5),
    ((True, False, True), "0", 0),
    ((True, True, False), "-5", -5),
    ((False, True, False), "-7", -7),
])
def test_int_odd_options(options, test_value, expected_results):
    test_type = argparse_custom_types.int_odd(*options)
    result = test_type(test_value)
    assert result == expected_results


@pytest.mark.parametrize("options, test_value", [
    ((True, False, False), "-7"),
    ((True, True, False), "8"),
    ((False, True, False), "7"),
    ((True, False, False), "0"),
])
def test_int_odd_options_fail(options, test_value):
    test_type = argparse_custom_types.int_odd(*options)
    with pytest.raises(argparse_custom_types.argparse.ArgumentTypeError):
        test_type(test_value)
