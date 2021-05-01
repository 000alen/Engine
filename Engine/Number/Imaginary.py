from Engine.Number import Skeleton
from Engine.Number.Real import Real, REAL_ZERO, REAL_ONE


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
