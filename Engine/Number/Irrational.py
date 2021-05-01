from Engine.Number import Skeleton


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
