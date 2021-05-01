from Engine.Algorithm.Division import number_division, number_floor_division
from Engine.Number.Operation import N

from abc import ABC, abstractmethod, abstractproperty, abstractclassmethod

DEFAULT_PRECISION = 15
DEFAULT_PRECISION_TAYLOR_POLYNOMIAL = 5


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
        return self.greater_equal(other)

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

    def __floordiv__(self, other):
        if type(other) is not type(self):
            other = self.upgrade(other)
        return self.floor_divide(other)

    def __mod__(self, other):
        if type(other) is not type(self):
            other = self.upgrade(other)
        return self.modulus(other)

    @classmethod
    def upgrade(cls, other):
        from Engine.Number.Natural import Natural
        from Engine.Number.Integer import Integer
        from Engine.Number.Rational import Rational
        from Engine.Number.Irrational import Irrational
        from Engine.Number.Real import Real
        from Engine.Number.Imaginary import Imaginary
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
    def real(self) -> "Number":
        return self

    @property
    def imaginary(self):
        return None

    @property
    def is_integer(self) -> bool:
        x = self.reduce()
        return x.exponent >= 0

    @property
    def is_fractional(self) -> bool:
        return not self.is_integer

    # TODO: See if there is a more efficient way to do this
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

    def greater(self, other: "Number") -> bool:
        return not self.equal(other) and not self.lower(other)

    def lower_equal(self, other: "Number") -> bool:
        return self.equal(other) or self.lower(other)

    def greater_equal(self, other: "Number") -> bool:
        return self.equal(other) or self.greater(other)

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

    # TODO: Implement efficient exponentiation
    def power(self, other: "Number") -> "Number":
        assert other.is_integer and other >= NUMBER_ZERO
        return Number(
            self.mantissa ** other.mantissa,
            self.exponent * other.mantissa
        )

    def invert(self, n: int = DEFAULT_PRECISION) -> "Number":
        if self == NUMBER_ZERO:
            raise ZeroDivisionError

        return number_division(NUMBER_ONE, self)

    def divide(self, other: "Number") -> "Number":
        if other == NUMBER_ZERO:
            raise ZeroDivisionError

        return number_division(self, other)

    def floor_divide(self, other: "Number") -> "Number":
        if other == NUMBER_ZERO:
            raise ZeroDivisionError

        return number_floor_division(self, other)

    def modulus(self, other: "Number") -> "Number":
        assert self.is_integer and self >= NUMBER_ZERO
        assert other.is_integer and other >= NUMBER_ZERO

        if other == NUMBER_ZERO:
            raise ZeroDivisionError

        return self - (other * self.floor_divide(other))


NUMBER_ZERO = Number(0, 0)
NUMBER_ONE = Number(1, 0)
