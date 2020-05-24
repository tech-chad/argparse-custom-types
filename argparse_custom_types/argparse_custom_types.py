""" argparse custom types"""
import argparse

from typing import Callable
from typing import List
from typing import Tuple
from typing import Union


def int_range(start: int, stop: int, step: int = 1) -> Callable:
    """ custom int in range from start to stop (not including)."""
    excepted_range = [x for x in range(start, stop, step)]

    def _int_range(value: str) -> int:
        error_msg = f"{value} is an invalid int value in range {start} - {stop}"
        try:
            int_value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(error_msg)
        else:
            if int_value not in excepted_range:
                raise argparse.ArgumentTypeError(error_msg)
            else:
                return int_value

    return _int_range


def int_above(minimum: int) -> Callable:
    """ int equal to or above minimum. """

    def _int_above(value: str) -> int:
        error_msg = f"{value} is an invalid int value above {minimum}"
        try:
            int_value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(error_msg)
        else:
            if int_value < minimum:
                raise argparse.ArgumentTypeError(error_msg)
            else:
                return int_value
    return _int_above


def int_below(maximum: int) -> Callable:
    """ int equal to or below maximum. """

    def _int_below(value: str) -> int:
        error_msg = f"{value} is an invalid int value below {maximum}"
        try:
            int_value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(error_msg)
        else:
            if int_value > maximum:
                raise argparse.ArgumentTypeError(error_msg)
            else:
                return int_value
    return _int_below


def in_sequence_strings(sequence: Union[Tuple[str], List[str]],
                        show_on_invalid: bool = False,
                        ) -> Callable:
    """
    excepts a value that is in the tuple or list and returns
    that value as a string
    """
    seq_string = ", ".join(sequence)

    def _in_sequence_strings(value: str) -> str:
        msg = f"{value} is not in the excepted value list"
        if show_on_invalid:
            error_msg = f"{msg}\n{seq_string}"
        else:
            error_msg = msg
        if value not in sequence:
            raise argparse.ArgumentTypeError(error_msg)
        else:
            return value

    return _in_sequence_strings

