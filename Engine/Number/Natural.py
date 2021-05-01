from Engine.Algorithm import natural_modulus
from Engine.Number import Skeleton, Number, NUMBER_ZERO, NUMBER_ONE


class Natural(Skeleton):
    __value: Number

    def __init__(self, value: Number):
        assert self.__is_valid_value(value)
        self.__value = value

    def __hash__(self):
        return hash(("Natural", self.value))

    def __str__(self) -> str:
        return f"{value}"

    @classmethod
    def __is_valid_value(cls, value: Number) -> bool:
        return value.is_integer and value >= NUMBER_ZERO

    @classmethod
    def from_string(cls, string: str) -> "Natural":
        return cls(Number.from_string(string))

    @classmethod
    def from_python_integer(cls, python_integer: int) -> "Natural":
        return cls(Number.from_python_integer(python_integer))

    @classmethod
    def from_number(cls, number: Number) -> "Natural":
        return cls(number)

    @property
    def value(self) -> "Number":
        return self.__value

    @property
    def real(self) -> "Natural":
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

    def equal(self, other: "Natural") -> bool:
        return self.value == other.value

    def lower(self, other: "Natural") -> bool:
        return self.value < other.value

    def greater(self, other: "Natural") -> bool:
        return self.value > other.value

    def lower_equal(self, other: "Natural") -> bool:
        return self.value <= other.value

    def greater_equal(self, other: "Natural") -> bool:
        return self.value >= other.value

    def absolute(self) -> "Natural":
        return self

    def add(self, other: "Natural") -> "Natural":
        return Natural(
            self.value + other.value
        )

    def subtract(self, other: "Natural") -> "Natural":
        return Natural(
            self.value - other.value
        )

    def multiply(self, other: "Natural") -> "Natural":
        return Natural(
            self.value * other.value
        )

    # TODO: Implement Efficient Exponentiation
    def power(self, other: "Natural") -> "Natural":
        return Natural(
            self.value ** other.value
        )

    def divide(self, other: "Natural") -> "Natural":
        return Natural(
            self.value / other.value
        )

    def floor_divide(self, other: "Natural") -> "Natural":
        return Natural(
            self.value // other.value
        )

    def modulus(self, other: "Natural") -> "Natural":
        return Natural(
            self.value % other.value
        )


NATURAL_ZERO = Natural(NUMBER_ZERO)
NATURAL_ONE = Natural(NUMBER_ONE)
