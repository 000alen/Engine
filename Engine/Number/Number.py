from Engine.Number import DEFAULT_PRECISION
from Engine.Number.Operation import N


class Numeric:
    __mantissa: int
    __exponent: int
    # __period: int

    def __init__(self, mantissa: int, exponent: int):  # , period: int = 0):
        # assert period >= 0
        self.__mantissa = mantissa
        self.__exponent = exponent
        # self.__period = period

    def __str__(self) -> str:
        return f"{self.mantissa}e{self.exponent}"

    @property
    def mantissa(self) -> int:
        return self.__mantissa

    @property
    def exponent(self) -> int:
        return self.__exponent

    # @property
    # def period(self) -> int:
    #     return self.__period

    def reduce(self) -> "Numeric":
        n = max(i for i in range(N(self.mantissa)) if abs(self.mantissa) % pow(10, i) == 0)

        mantissa = abs(self.mantissa) // pow(10, n)
        exponent = self.exponent + n

        return Numeric(
            mantissa,
            exponent
        )

    def equals(self, other: "Numeric") -> bool:
        x = self.reduce()
        y = other.reduce()
        
        return x.mantissa == y.mantissa and x.exponent == y.exponent

    def absolute(self) -> "Numeric":
        return Numeric(
            abs(self.mantissa),
            self.exponent
        )

    def add(self, other: "Numeric") -> "Numeric":
        minimun_exponent = min(self.exponent, other.exponent)
        return Numeric(
            (self.mantissa * pow(10, self.exponent - minimun_exponent)) +
            (other.mantissa * pow(10, other.exponent - minimun_exponent)),
            minimun_exponent
        )

    def negate(self) -> "Numeric":
        return Numeric(
            -self.mantissa,
            self.exponent
        )

    def subtract(self, other: "Numeric") -> "Numeric":
        return self.add(other.negate())

    def multiply(self, other: "Numeric") -> "Numeric":
        return Numeric(
            self.mantissa * other.mantissa,
            self.exponent + other.exponent
        )

    def invert(self, n: int = DEFAULT_PRECISION) -> "Numeric":
        if self.mantissa == 0:
            raise ZeroDivisionError

        quotient = []
        exponent = N(self.mantissa)
        delta_exponent = 0
        dividend = pow(10, exponent)
        dividend_history = []

        i = 0
        while dividend > 0:
            i += 1

            while dividend < abs(self.mantissa):
                dividend *= 10
                delta_exponent += 1

            quotient.append(max(q for q in range(1, 10)
                            if dividend - (q * abs(self.mantissa)) >= 0))
            dividend -= quotient[-1] * abs(self.mantissa)
            exponent += delta_exponent
            delta_exponent = 0

            if dividend not in dividend_history:
                dividend_history.append(dividend)
            elif i >= n:
                break

        quotient = sum(digit * pow(10, i)
                       for i, digit in enumerate(reversed(quotient)))

        return Numeric(
            quotient,
            -self.exponent - exponent
        )

    def divide(self, other: "Numeric") -> "Numeric":
        return self.multiply(other.invert())


NUMERIC_ZERO = Numeric(0, 0)


class Complex:
    __real: Numeric
    __imaginary: Numeric

    def __init__(self, real: Numeric, imaginary: Numeric):
        self.__real = real
        self.__imaginary = imaginary

    @property
    def real(self):
        return self.__real

    @property
    def imaginary(self):
        return self.__imaginary


class Real(Complex):
    __imaginary: Numeric = NUMERIC_ZERO

    def __init__(self, real: Numeric):
        self.__real = real


class Imaginary(Complex):
    __real: Numeric = NUMERIC_ZERO

    def __init__(self, imaginary: Numeric):
        self.__imaginary = imaginary


class Rational(Real):
    pass


class Irrational(Real):
    pass


class Integer(Rational):
    pass


class Natural(Integer):
    pass
