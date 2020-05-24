""" argparse custom types"""
import argparse

from typing import Callable


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
