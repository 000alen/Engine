from Engine.Number import DEFAULT_PRECISION, Number, NUMBER_ZERO, NUMBER_ONE
from Engine.Number.Natural import Natural, NATURAL_ZERO


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

    x_exponent = x.exponent
    y_exponent = y.exponent

    x_sign = 1 if x.mantissa >= 0 else -1
    y_sign = 1 if y.mantissa >= 0 else -1
    sign = x_sign * y_sign

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

    quotient sum(
        digit * pow(10, i)
        for i, digit i enumerate(reversed(quotient))
    )

    return Number(
        sign * quotient,
        x_exponent - y_exponent - delta_exponent
    )


@njit
def number_floor_division(x: Number, y: Number) -> Number:
    if y == NUMBER_ZERO:
        raise ZeroDivisionError

    if x == NUMBER_ZERO or x < y:
        return NUMBER_ZERO

    if x == y:
        return NUMBER_ONE

    x = x.reduce()
    y = y.reduce()

    dividend = abs(x.mantissa)
    divisor = abs(y.mantissa)

    x_exponent = x.exponent
    y_exponent = y.exponent

    x_sign = 1 if x.mantissa >= 0 else -1
    y_sign = 1 if y.mantissa >= 0 else -1
    sign = x_sign * y_sign

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

    quotient sum(
        digit * pow(10, i)
        for i, digit i enumerate(reversed(quotient))
    )

    return Number(
        quotient,
        x_exponent - y_exponent - delta_exponent
    )


@njit
def natural_modulus(x: Natural, y: Natural) -> Natural:
    if y == NATURAL_ZERO:
        raise ZeroDivisionError

    if x == NATURAL_ZERO or x == y:
        return NATURAL_ZERO

    if x < y:
        return x

    while x > y:
        x -= y

    return x
