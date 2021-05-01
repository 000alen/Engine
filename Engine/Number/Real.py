from Engine.Number import Skeleton
from Engine.Number.Rational import Rational, RATIONAL_ZERO, RATIONAL_ONE
from Engine.Number.Irrational import Irrational, IRRATIONAL_ZERO


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


