from Engine.Number import Skeleton, Number, NUMBER_ZERO, NUMBER_ONE
from Engine.Number.Natural import Natural


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
    def from_string(cls, string: str) -> "Integer":
        return cls(Number.from_string(string))

    @classmethod
    def from_python_integer(cls, python_integer: int) -> "Integer":
        return cls(Number.from_python_integer(python_integer))

    @classmethod
    def from_number(cls, number: Number) -> "Integer":
        return cls(number)

    @classmethod
    def from_natural(cls, natural: Natural) -> "Integer":
        return cls(natural.value)

    @property
    def value(self) -> Number:
        return self.__value

    @property
    def real(self) -> "Integer":
        return self

    @property
    def imaginary(self):
        return None

    @property
    def is_integer(self) -> bool:
        return True

    @property
    def is_fractional(self) -> bool:
        return False

    def equal(self, other: "Integer") -> bool:
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


INTEGER_ZERO = Integer(NUMBER_ZERO)
INTEGER_ONE = Integer(NUMBER_ONE)
