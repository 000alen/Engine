from Engine.Number import DEFAULT_PRECISION
from Engine.Number.Operation import N

from typing import Union
from abc import ABC, abstractmethod, abstractproperty, abstractclassmethod

__all__ = (
    "Number",
    "Natural",
    "Integer",
    "Rational",
    "Irrational",
    "Real",
    "Complex",

    "NUMBER_ZERO",
    "NUMBER_ONE",
    "NATURAL_ZERO",
    "NATURAL_ONE",
    "INTEGER_ZERO",
    "INTEGER_ONE",
    "RATIONAL_ZERO",
    "RATIONAL_ONE",
    "IRRATIONAL_ZERO",
    "IRRATIONAL_ONE"
    "REAL_ZERO",
    "REAL_ONE",
    "IMAGINARY_ZERO",
    "IMAGINARY_ONE",
    "I",
    "COMPLEX_ZERO",
    "COMPLEX_ONE",
    "COMPLEX_I"
)

NumberSupported = Union["Number", str, int]


class Skeleton(ABC):
    def __eq__(self, other):
        if type(other) is not type(self):
            other = self.upgrade(other)
        return self.equal(other)

    def __ne__(self, other):
        if type(other) is not type(self):
            other = self.upgrade(other)
        return not self.equal(other)

    def __lt__(self, other):
        if type(other) is not type(self):
            other = self.upgrade(other)
        return self.lower(other)

    def __gt__(self, other):
        if type(other) is not type(self):
            other = self.upgrade(other)
        return self.greater(other)

    def __le__(self, other):
        if type(other) is not type(self):
            other = self.upgrade(other)
        return self.lower_equal(other)

    def __ge__(self, other):
        if type(other) is not type(self):
            other = self.upgrade(other)
        return self.greather_equal(other)

    def __abs__(self):
        return self.absolute()

    def __add__(self, other):
        if type(other) is not type(self):
            other = self.upgrade(other)
        return self.add(other)

    def __neg__(self):
        return self.negate()

    def __sub__(self, other):
        if type(other) is not type(self):
            other = self.upgrade(other)
        return self.subtract(other)

    def __mul__(self, other):
        if type(other) is not type(self):
            other = self.upgrade(other)
        return self.multiply(other)

    def __pow__(self, other):
        if type(other) is not type(self):
            other = self.upgrade(other)
        return self.power(other)

    def __truediv__(self, other):
        if type(other) is not type(self):
            other = self.upgrade(other)
        return self.divide(other)

    @classmethod
    def upgrade(cls, other):
        wrapper = {
            cls: lambda x: x,
            str: cls.from_string,
            int: cls.from_python_integer,
            Number: cls.from_number,
            Natural: cls.from_natural,
            Integer: cls.from_integer,
            Rational: cls.from_rational,
            Irrational: cls.from_irrational,
            Real: cls.from_real,
            Imaginary: cls.from_imaginary
        }
        try:
            return wrapper[type(other)](other)
        except:
            raise Exception

    @abstractproperty
    def real(self):
        raise NotImplementedError

    @abstractproperty
    def imaginary(self):
        raise NotImplementedError


class Number(Skeleton):
    __mantissa: int
    __exponent: int

    def __init__(self, mantissa: int, exponent: int):
        self.__mantissa = mantissa
        self.__exponent = exponent

    def __hash__(self):
        x = self.reduce()
        return hash(("Number", x.mantissa, x.exponent))

    def __str__(self) -> str:
        return f"{self.mantissa}e{self.exponent}"

    @classmethod
    def from_string(cls, string: str) -> "Number":
        if "e" in string:
            mantissa, exponent = [int(_) for _ in string.split("e")]
            return cls(
                mantissa,
                exponent
            )
        elif "." in string:
            _, fractional = [int(_) for _ in string.split(".")]
            return cls(
                int(string.replace(".", "")),
                -N(fractional)
            )
        else:
            raise Exception

    @classmethod
    def from_python_integer(cls, python_integer: int) -> "Number":
        return cls(
            python_integer,
            0
        )

    @property
    def mantissa(self) -> int:
        return self.__mantissa

    @property
    def exponent(self) -> int:
        return self.__exponent

    @property
    def real(self):
        return self

    @property
    def imaginary(self):
        return None

    @property
    def is_integer(self):
        x = self.reduce()
        return x.exponent >= 0

    @property
    def is_fractional(self):
        return not self.is_integer

    def reduce(self) -> "Number":
        n = max(i for i in range(N(self.mantissa))
                if abs(self.mantissa) % pow(10, i) == 0)

        mantissa = abs(self.mantissa) // pow(10, n)
        exponent = self.exponent + n

        return Number(
            mantissa,
            exponent
        )

    def equal(self, other: "Number") -> bool:
        x = self.reduce()
        y = other.reduce()

        return x.mantissa == y.mantissa and x.exponent == y.exponent

    def lower(self, other: "Number") -> bool:
        x = self.reduce()
        y = other.reduce()

        minimum_exponent = min(x.exponent, y.exponent)

        x_mantissa = x.mantissa * pow(10, x.exponent - minimum_exponent)
        y_mantissa = y.mantissa * pow(10, y.exponent - minimum_exponent)

        return x_mantissa < y_mantissa

    def greather(self, other: "Number") -> bool:
        return not self.equal(other) and not self.lower(other)

    def lower_equal(self, other: "Number") -> bool:
        return self.equal(other) or self.lower(other)

    def greather_equal(self, other: "Number") -> bool:
        return self.equal(other) or self.greather(other)

    def absolute(self) -> "Number":
        return Number(
            abs(self.mantissa),
            self.exponent
        )

    def add(self, other: "Number") -> "Number":
        minimun_exponent = min(self.exponent, other.exponent)
        return Number(
            (self.mantissa * pow(10, self.exponent - minimun_exponent)) +
            (other.mantissa * pow(10, other.exponent - minimun_exponent)),
            minimun_exponent
        )

    def negate(self) -> "Number":
        return Number(
            -self.mantissa,
            self.exponent
        )

    def subtract(self, other: "Number") -> "Number":
        return self.add(other.negate())

    def multiply(self, other: "Number") -> "Number":
        return Number(
            self.mantissa * other.mantissa,
            self.exponent + other.exponent
        )

    def power(self, other: "Number") -> "Number":
        assert other.is_integer and other >= NUMBER_ZERO
        return Number(
            self.mantissa ** other.mantissa,
            self.exponent * other.mantissa
        )

    def invert(self, n: int = DEFAULT_PRECISION) -> "Number":
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

            if N(dividend) < N(self.mantissa):
                dividend *= pow(10, N(self.mantissa) - N(dividend))

            if dividend < abs(self.mantissa):
                dividend *= 10

            quotient.append(dividend // abs(self.mantissa))

            dividend -= quotient[-1] * abs(self.mantissa)
            exponent += delta_exponent
            delta_exponent = 0

            if dividend not in dividend_history:
                dividend_history.append(dividend)
            elif i >= n:
                break

        quotient = sum(digit * pow(10, i)
                       for i, digit in enumerate(reversed(quotient)))

        return Number(
            quotient if self.mantissa > 0 else -quotient,
            -self.exponent - exponent
        )

    def divide(self, other: "Number") -> "Number":
        return self.multiply(other.invert())


NUMBER_ZERO = Number(0, 0)
NUMBER_ONE = Number(1, 0)


class Natural(Skeleton):
    __value: Number

    def __init__(self, value: Number):
        assert self.__is_valid_value(value)
        self.__value = value

    def __hash__(self):
        return hash(("Natural", self.value))

    def __str__(self):
        return f"{value}"

    @classmethod
    def __is_valid_value(cls, value: Number) -> bool:
        return value.is_integer and value >= NUMBER_ZERO

    @classmethod
    def from_string(cls, string):
        return cls(Number.from_string(string))

    @classmethod
    def from_python_integer(cls, python_integer):
        return cls(Number.from_python_integer(python_integer))

    @classmethod
    def from_number(cls, number):
        return cls(number)

    @property
    def value(self):
        return self.__value

    @property
    def real(self):
        return self

    @property
    def imaginary(self):
        return None


NATURAL_ZERO = Natural(NUMBER_ZERO)
NATURAL_ONE = Natural(NUMBER_ONE)


class Integer(Skeleton):
    __value: Number

    def __init__(self, value: Number):
        assert self.__is_valid_value(value)
        self.__value = value

    def __hash__(self):
        return hash(("Integer", self.value))

    def __str__(self):
        return f"{self.value}"

    @classmethod
    def __is_valid_value(cls, value: Number) -> bool:
        return value.is_integer

    @classmethod
    def from_string(cls, string):
        return cls(Number.from_string(string))

    @classmethod
    def from_python_integer(cls, python_integer):
        return cls(Number.from_python_integer(python_integer))

    @classmethod
    def from_number(cls, number):
        return cls(number)

    @classmethod
    def from_natural(cls, natural):
        return cls(natural.value)

    @property
    def value(self):
        return self.__value

    @property
    def real(self):
        return self

    @property
    def imaginary(self):
        return None


INTEGER_ZERO = Integer(NUMBER_ZERO)
INTEGER_ONE = Integer(NUMBER_ONE)


class Rational(Skeleton):
    __numerator: Integer
    __denominator: Integer

    def __init__(self, numerator: Integer, denominator: Integer):
        assert denominator != INTEGER_ZERO
        self.__numerator = numerator
        self.__denominator = denominator

    def __hash__(self):
        return hash(("Rational", self.numerator, self.denominator))

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

        @classmethod
    @classmethod
    def from_string(cls, string):
        return cls(Integer.from_string(string), INTEGER_ONE)

    @classmethod
    def from_python_integer(cls, python_integer):
        return cls(Integer.from_python_integer(python_integer), INTEGER_ONE)

    @classmethod
    def from_number(cls, number):
        return cls(Integer.from_number(number), INTEGER_ONE)

    @classmethod
    def from_natural(cls, natural):
        return cls(Integer.from_natural(natural), INTEGER_ONE)

    @classmethod
    def from_integer(cls, integer):
        return cls(integer, INTEGER_ONE)

    @property
    def numerator(self):
        return self.__numerator

    @property
    def denominator(self):
        return self.__denominator

    @property
    def real(self):
        return self

    @property
    def imaginary(self):
        return None


RATIONAL_ZERO = Rational(INTEGER_ZERO, INTEGER_ONE)
RATIONAL_ONE = Rational(INTEGER_ONE, INTEGER_ONE)


class Irrational(Skeleton):
    # __generator: Function

    def __init__(self, generator):
        self.__generator = generator

    def __hash__(self):
        return hash("Irrational", self.generator)

    # def __str__(self):
    #     return f"{self.compute()}..."

    @property
    def generator(self):
        return self.__generator

    @property
    def real(self):
        return self

    @property
    def imaginary(self):
        return None


IRRATIONAL_ZERO = Irrational(lambda: 0)
IRRATIONAL_ONE = Irrational(lambda: 1)


class Real(Skeleton):
    __rational: Rational
    __irrational: Irrational

    def __init__(self, rational: Rational = None, irrational: Irrational = None):
        assert rational != irrational != None
        self.__rational = rational
        self.__irrational = irrational

    def __hash__(self):
        return hash(("Real", self.rational, self.irrational))

    # def __str__(self):
    #     return f"{self.compute()}"

    @classmethod
    def from_string(cls, string):
        return cls(Rational.from_string(string), IRRATIONAL_ZERO)

    @classmethod
    def from_python_integer(cls, python_integer):
        return cls(Rational.from_python_integer(python_integer), IRRATIONAL_ZERO)

    @classmethod
    def from_number(cls, number):
        return cls(Rational.from_number(number), IRRATIONAL_ZERO)

    @classmethod
    def from_natural(cls, natural):
        return cls(Rational.from_natural(natural), IRRATIONAL_ZERO)

    @classmethod
    def from_integer(cls, integer):
        return cls(Rational.from_integer(integer), IRRATIONAL_ZERO)

    @classmethod
    def from_rational(cls, rational):
        return cls(rational, IRRATIONAL_ZERO)

    @classmethod
    def from_irrational(cls, irrational):
        return cls(RATIONAL_ZERO, irrational)

    @property
    def rational(self):
        return self.__rational

    @property
    def irrational(self):
        return self.__irrational

    @property
    def real(self):
        return self

    @property
    def imaginary(self):
        return None


REAL_ZERO = Real(RATIONAL_ZERO)
REAL_ONE = Real(RATIONAL_ONE)


class Imaginary(Skeleton):
    __value: Real

    def __init__(self, value: Real):
        self.__value = value

    def __hash__(self):
        return hash(("Imaginary", self.value))

    @property
    def value(self):
        pass

    @property
    def real(self):
        return None

    @property
    def imaginary(self):
        return self


IMAGINARY_ZERO = Imaginary(REAL_ZERO)
IMAGINARY_ONE = Imaginary(REAL_ONE)
I = IMAGINARY_ONE


class Complex(Skeleton):
    __real: Real
    __imaginary: Imaginary

    def __init__(self, real: Real, imaginary: Imaginary):
        self.__real = real
        self.__imaginary = imaginary

    def __hash__(self):
        return hash(("Complex", self.real, self.imaginary))

    def __str__(self):
        pass

    @classmethod
    def from_string(cls, string):
        return cls(Real.from_string(string), IMAGINARY_ZERO)

    @classmethod
    def from_python_integer(cls, python_integer):
        return cls(Real.from_python_integer(python_integer), IMAGINARY_ZERO)

    @classmethod
    def from_number(cls, number):
        return cls(Real.from_number(number), IMAGINARY_ZERO)

    @classmethod
    def from_natural(cls, natural):
        return cls(Real.from_natural(natural), IMAGINARY_ZERO)

    @classmethod
    def from_integer(cls, integer):
        return cls(Real.from_integer(integer), IMAGINARY_ZERO)

    @classmethod
    def from_rational(cls, rational):
        return cls(Real.from_rational(rational), IMAGINARY_ZERO)

    @classmethod
    def from_irrational(cls, irrational):
        return cls(Real.from_irrational(irrational), IMAGINARY_ZERO)

    @classmethod
    def from_real(cls, real):
        return cls(real, IMAGINARY_ZERO)

    @classmethod
    def from_imaginary(cls, imaginary):
        return cls(REAL_ZERO, imaginary)

    @property
    def real(self):
        return self.__real

    @property
    def imaginary(self):
        return self.__imaginary


COMPLEX_ZERO = Complex(REAL_ZERO, IMAGINARY_ZERO)
COMPLEX_ONE = Complex(REAL_ONE, IMAGINARY_ZERO)
COMPLEX_I = Complex(REAL_ZERO, IMAGINARY_ONE)
