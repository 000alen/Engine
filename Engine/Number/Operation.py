from Engine.Number import DEFAULT_PRECISION

from math import floor, log


def N(x: int) -> int:
    return floor(log(abs(x), 10)) + 1


def integer_division(x: int, y: int) -> int:
    assert y != 0

    if x < y:
        return 0

    if x == y:
        return 1

    quotient = []
    while x > 0 and x >= y:
        quotient.append(max(i for i in range(1, 10) if i * y <= x))
        x -= quotient[-1] * y

    return sum(digit * pow(10, i)
               for i, digit in enumerate(reversed(quotient)))
