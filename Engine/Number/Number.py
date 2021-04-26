from Engine.Number import DEFAULT_PRECISION
from Engine.Number.Operation import N

from typing import Union

NumericSupported = Union["Numeric", str, int]


class Numeric:
    __mantissa: int
    __exponent: int

    def __init__(self, mantissa: int, exponent: int):
        self.__mantissa = mantissa
        self.__exponent = exponent

    def __str__(self) -> str:
        return f"{self.mantissa}e{self.exponent}"

    def __eq__(self, other: NumericSupported) -> bool:
        other = Numeric.convert(other)
        return self.equal(other)

    def __ne__(self, other: NumericSupported) -> bool:
        other = Numeric.convert(other)
        return not self.equal(other)

    def __lt__(self, other: NumericSupported) -> bool:
        other = Numeric.convert(other)
        return self.lower_than(other)

    def __gt__(self, other: NumericSupported) -> bool:
        other = Numeric.convert(other)
        return self.greather_than(other)

    def __le__(self, other: NumericSupported) -> bool:
        other = Numeric.convert(other)
        return self.lower_equal(other)

    def __ge__(self, other: NumericSupported) -> bool:
        other = Numeric.convert(other)
        return self.greather_equal(other)

    def __abs__(self) -> "Numeric":
        return self.absolute

    def __add__(self, other: NumericSupported) -> "Numeric":
        other = Numeric.convert(other)
        return self.add(other)

    def __neg__(self) -> "Numeric":
        return self.negate()

    def __sub__(self, other: NumericSupported) -> "Numeric":
        other = Numeric.convert(other)
        return self.subtract(other)

    def __mul__(self, other: NumericSupported) -> "Numeric":
        other = Numeric.convert(other)
        return self.multiply(other)

    def __pow__(self, other: int) -> "Numeric":
        return self.natural_power(other)

    def __truediv__(self, other: NumericSupported) -> "Numeric":
        other = Numeric.convert(other)
        return self.divide(other)

    @classmethod
    def convert(cls, other: NumericSupported) -> "Numeric":
        if type(other) is Numeric:
            return other
        elif type(other) is str:
            return Numeric.from_string(other)
        elif type(other) is int:
            return Numeric.from_integer(other)
        else:
            raise Exception

    @classmethod
    def from_string(cls, string: str) -> "Numeric":
        if "e" in string:
            mantissa, exponent = [int(_) for _ in string.split("e")]
            return Numeric(
                mantissa,
                exponent
            )
        elif "." in string:
            _, fractional = [int(_) for _ in string.split(".")]
            return Numeric(
                int(string.replace(".", "")),
                -N(fractional)
            )
        else:
            raise Exception

    @classmethod
    def from_integer(cls, integer: int) -> "Numeric":
        return Numeric(
            integer,
            0
        )

    @property
    def mantissa(self) -> int:
        return self.__mantissa

    @property
    def exponent(self) -> int:
        return self.__exponent

    def reduce(self) -> "Numeric":
        n = max(i for i in range(N(self.mantissa))
                if abs(self.mantissa) % pow(10, i) == 0)

        mantissa = abs(self.mantissa) // pow(10, n)
        exponent = self.exponent + n

        return Numeric(
            mantissa,
            exponent
        )

    def equal(self, other: "Numeric") -> bool:
        x = self.reduce()
        y = other.reduce()

        return x.mantissa == y.mantissa and x.exponent == y.exponent

    def lower_than(self, other: "Numeric") -> bool:
        x = self.reduce()
        y = other.reduce()

        minimum_exponent = min(x.exponent, y.exponent)

        x_mantissa = x.mantissa * pow(10, x.exponent - minimum_exponent)
        y_mantissa = y.mantissa * pow(10, y.exponent - minimum_exponent)

        return x_mantissa < y_mantissa

    def greather_than(self, other: "Numeric") -> bool:
        return not self.lower_than(other) and not self.equal(other)

    def lower_equal(self, other: "Numeric") -> bool:
        return self.lower_than(other) or self.equal(other)

    def greather_equal(self, other: "Numeric") -> bool:
        return self.greather_than(other) or self.equal(other)

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

    def natural_power(self, other: int) -> "Numeric":
        assert other >= 0
        return Numeric(
            self.mantissa ** other,
            self.exponent * other
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
NUMERIC_ONE = Numeric(1, 0)


class Complex:
    __real: Numeric
    __imaginary: Numeric

    def __init__(self, real: Numeric, imaginary: Numeric):
        self.__real = real
        self.__imaginary = imaginary

    def __str__(self):
        return f"{self.real} + {self.imaginary}i"

    def __eq__(self, other):
        return self.equal(other)

    def __ne__(self, other):
        return not self.equal(other)

    def __abs__(self):
        return self.absolute()

    def __add__(self, other):
        return self.add(other)

    def __neg__(self):
        return self.negate()

    def __sub__(self, other):
        return self.subtract(other)

    def __mul__(self, other):
        return self.multiply(other)

    def __truediv__(self, other):
        return self.divide(other)

    @property
    def real(self):
        return self.__real

    @property
    def imaginary(self):
        return self.__imaginary

    def equal(self, other):
        return self.real == other.real and self.imaginary == other.imaginary

    def absolute(self):
        # TODO: Implement square root
        raise NotImplementedError

    def add(self, other):
        return Complex(
            self.real + other.real,
            self.imaginary + other.imaginary
        )

    def negate(self):
        return Complex(
            -self.real,
            -self.imaginary
        )

    def conjugate(self):
        return Complex(
            self.real,
            -self.imaginary
        )

    def multiply(self, other):
        return Complex(
            self.real * other.imaginary - self.imaginary * other.imaginary,
            self.real * other.imaginary + self.imaginary * other.real
        )

    def invert(self):
        assert self.real ** 2 + self.imaginary ** 2 > NUMERIC_ZERO

        return Complex(
            self.real / (self.real ** 2 + self.imaginary ** 2),
            -self.imaginary / (self.real ** 2 + self.imaginary ** 2)
        )

    def divide(self, other):
        return self.multiply(other.invert())


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
