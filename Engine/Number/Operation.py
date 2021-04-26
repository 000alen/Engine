from Engine.Number import DEFAULT_PRECISION

from math import floor, log


def N(x: int) -> int:
    return floor(log(abs(x), 10)) + 1
