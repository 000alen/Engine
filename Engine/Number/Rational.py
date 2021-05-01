from Engine.Number import Skeleton, Number
from Engine.Number.Natural import Natural
from Engine.Number.Integer import Integer, INTEGER_ZERO, INTEGER_ONE


class Rational(Skeleton):
    __numerator: Integer
    __denominator: Integer

    def __init__(self, numerator: Integer, denominator: Integer):
        assert denominator != INTEGER_ZERO
        self.__numerator = numerator
        self.__denominator = denominator

    def __hash__(self):
        return hash(("Rational", self.numerator, self.denominator))

    def __str__(self) -> str:
        return f"{self.numerator}/{self.denominator}"

        @classmethod
    @classmethod
    def from_string(cls, string: str) -> "Rational":
        return cls(Integer.from_string(string), INTEGER_ONE)

    @classmethod
    def from_python_integer(cls, python_integer: int) "Rational":
        return cls(Integer.from_python_integer(python_integer), INTEGER_ONE)

    @classmethod
    def from_number(cls, number: Number) -> "Rational":
        return cls(Integer.from_number(number), INTEGER_ONE)

    @classmethod
    def from_natural(cls, natural: Natural) -> "Rational":
        return cls(Integer.from_natural(natural), INTEGER_ONE)

    @classmethod
    def from_integer(cls, integer: Integer) -> "Rational":
        return cls(integer, INTEGER_ONE)

    @property
    def numerator(self) -> "Integer":
        return self.__numerator

    @property
    def denominator(self) -> "Integer":
        return self.__denominator

    @property
    def real(self) -> "Rational":
        return self

    @property
    def imaginary(self):
        return None

    def reduce(self) -> "Rational":
        pass

    def equal(self, other: "Rational") -> bool:
        return self.value == other.value

    def lower(self, other: "Integer") -> bool:
        return self.value < other.value

    def greater(self, other: "Integer") -> bool:
        return self.value > other.value

    def lower_equal(self, other: "Integer") -> bool:
        return self.value <= other.value

    def greater_equal(self, other: "Integer") -> bool:
        return self.value >= other.value

    def absolute(self) -> "Integer":
        return Integer(
            abs(self.value)
        )

    def add(self, other: "Integer") -> "Integer":
        return Natural(
            self.value + other.value
        )

    def negate(self): "Integer":
        return Integer(
            -self.value
        )

    def subtract(self, other: "Integer") -> "Integer":
        return Natural(
            self.value - other.value
        )

    def multiply(self, other: "Integer") -> "Integer":
        return Natural(
            self.value * other.value
        )

    def power(self, other: "Integer") -> "Integer":
        assert other >= 0
        return Natural(
            self.value ** other.value
        )

    def divide(self, other: "Integer") -> "Integer":
        return Natural(
            self.value / other.value
        )


RATIONAL_ZERO = Rational(INTEGER_ZERO, INTEGER_ONE)
RATIONAL_ONE = Rational(INTEGER_ONE, INTEGER_ONE)
