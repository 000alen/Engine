from Engine.Number import Skeleton
from Engine.Number.Real import Real, REAL_ZERO, REAL_ONE
from Engine.Number.Imaginary import Imaginary, IMAGINARY_ZERO, IMAGINARY_ONE


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
