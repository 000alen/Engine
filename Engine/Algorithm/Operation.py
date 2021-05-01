from Engine.Number import DEFAULT_PRECISION_TAYLOR_POLYNOMIAL

from functools import cache
from math import floor, log
from numba import njit


@cache
def N(x: int) -> int:
    if x == 0:
        return 1
    return floor(log(abs(x), 10)) + 1


@njit
def factorial(x: "Numeric") -> "Numeric":
    from Engine.Number.Number import NUMERIC_ONE
    y = NUMERIC_ONE
    i = NUMERIC_ONE
    while i <= x:
        y *= i
        i += NUMERIC_ONE
    return y


@njit
def sin(x: "Numeric", n: int = DEFAULT_PRECISION_TAYLOR_POLYNOMIAL) -> "Numeric":
    from Engine.Number.Number import Numeric, NUMERIC_ZERO

    y = NUMERIC_ZERO
    for i in range(n):
        y += (Numeric(-1, 0) ** i) / \
            factorial(Numeric((2 * i) + 1, 0)) * (x ** ((2 * i) + 1))
    return y


@njit
def cos(x: "Numeric", n: int = DEFAULT_PRECISION_TAYLOR_POLYNOMIAL) -> "Numeric":
    from Engine.Number.Number import Numeric, NUMERIC_ZERO

    y = NUMERIC_ZERO
    for i in range(n):
        y += (Numeric(-1, 0) ** i) / \
            factorial(Numeric(2 * i, 0)) * (x ** (2 * i))
    return y


@njit
def exp(x: "Numeric", n: int = DEFAULT_PRECISION_TAYLOR_POLYNOMIAL) -> "Numeric":
    raise NotImplementedError
