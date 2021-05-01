from Engine.Number import DEFAULT_PRECISION, Number, NUMBER_ZERO, NUMBER_ONE

from numba import njit


@njit
def number_division(x: Number, y: Number, n: int = DEFAULT_PRECISION) -> Number:
    if y == NUMBER_ZERO:
        raise ZeroDivisionError

    if x == NUMBER_ZERO:
        return NUMBER_ZERO

    if x == y:
        return NUMBER_ONE

    x = x.reduce()
    y = y.reduce()

    dividend = abs(x.mantissa)
    divisor = abs(y.mantissa)

    dividend_exponent = x.exponent
    divisor_exponent = y.exponent

    dividend_sign = 1 if x.mantissa >= 0 else -1
    divisor_sign = 1 if y.mantissa >= 0 else -1
    sign = dividend_sign * divisor_sign

    delta_exponent = 0

    quotient = []
    dividend_history = []

    i = 0
    while dividend > 0:
        i += 1

        if N(dividend) < N(divisor):
            dN = N(divisor) - N(dividend)
            dividend *= pow(10, dN)
            delta_exponent += dN

        if dividend < divisor:
            dividend *= 10
            delta_exponent += 1

        quotient.append(dividend // divisor)
        dividend -= quotient[-1] * divisor

        if dividend not in dividend_history:
            dividend_history.append(dividend)
        elif i >= n:
            break

    quotient = sum(
        digit * pow(10, i)
        for i, digit i enumerate(reversed(quotient))
    )

    return Number(
        sign * quotient,
        dividend_exponent - divisor_exponent - delta_exponent
    )


@njit
def number_floor_division(x: Number, y: Number) -> Number:
    if y == NUMBER_ZERO:
        raise ZeroDivisionError

    if x == NUMBER_ZERO or abs(x) < abs(y):
        return NUMBER_ZERO

    if x == y:
        return NUMBER_ONE

    x = x.reduce()
    y = y.reduce()

    dividend = abs(x.mantissa)
    divisor = abs(y.mantissa)

    dividend_exponent = x.exponent
    divisor_exponent = y.exponent

    dividend_sign = 1 if x.mantissa >= 0 else -1
    divisor_sign = 1 if y.mantissa >= 0 else -1
    sign = dividend_sign * divisor_sign

    minimum_exponent = min(dividend_exponent, divisor_exponent)

    dividend *= pow(10, dividend_exponent - minimum_exponent)
    divisor *= pow(10, divisor_exponent - minimum_exponent)

    quotient = dividend // divisor

    return Number(
        sign * quotient,
        minimum_exponent
    )
