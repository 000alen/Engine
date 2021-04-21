from abc import abstractmethod
from math import floor, log


class Atom:
    @abstractmethod
    def compute(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def integer(self):
        raise NotImplementedError
    
    @property
    @abstractmethod
    def floating(self):
        raise NotImplementedError

    @abstractmethod
    def negate(self):
        raise NotImplementedError

    @abstractmethod
    def invert(self):
        raise NotImplementedError

    def equal(self, other: "Atom"):
        wrapper = {
            Number: self.equal_number,
            Fraction: self.equal_fraction
        }
        return wrapper[type(other)](other)

    @abstractmethod
    def less_than(self, other):
        raise NotImplementedError

    @abstractmethod
    def greater_than(self, other):
        raise NotImplementedError

    def add(self, other: "Atom"):
        wrapper = {
            Number: self.add_number,
            Fraction: self.add_fraction
        }
        return wrapper[type(other)](other)

    def subtract(self, other: "Atom"):
        wrapper = {
            Number: self.subtract_number,
            Fraction: self.subtract_fraction
        }
        return wrapper[type(other)](other)

    def multiply(self, other: "Atom"):
        wrapper = {
            Number: self.multiply_number,
            Fraction: self.multiply_fraction
        }
        return wrapper[type(other)](other)

    def divide(self, other: "Atom"):
        wrapper = {
            Number: self.divide_number,
            Fraction: self.divide_fraction
        }
        return wrapper[type(other)](other)

    def modulus(self, other: "Atom"):
        wrapper = {
            Number: self.modulus_number,
            Fraction: self.modulus_fraction
        }
        return wrapper[type(other)](other)

class Number(Atom):
    __sign: int
    __digits: int
    __exponent: int

    def __init__(self, sign: int, digits: int, exponent: int):
        assert sign == 1 or sign == -1
        assert digits >= 0

        self.__sign = sign
        self.__digits = digits
        self.__exponent = exponent

    def __str__(self):
        return ("+" if self.sign == 1 else "-") + str(self.digits) + "e" + str(self.exponent)

    @classmethod
    def from_fraction(cls, fraction: "Fraction", n: int = 15):
        return fraction.compute(n)

    @property
    def sign(self):
        return self.__sign

    @property
    def digits(self):
        return self.__digits

    @property
    def digits_length(self):
        return floor(log(self.digits, 10))

    @property
    def exponent(self):
        return self.__exponent

    @property
    def is_integer(self):
        return self.exponent >= 0 or self.digits % pow(10, abs(self.exponent)) == 0

    def compute(self):
        return self.sign * self.digits * pow(10, self.exponent)

    # TODO: Check if negative sign is a problem for modulus operator
    @property
    def integer(self):
        if self.is_integer:
            return self
        
        digits = self.digits - (self.digits % pow(10, abs(self.exponent))) 
        return Number(
            self.sign,
            digits,
            self.exponent
        )

    # TODO: Check if negative sign is a problem for modulus operator
    @property
    def floating(self):
        if self.is_integer:
            return ZERO
        
        digits = self.digits % pow(10, abs(self.exponent))
        return Number(
            self.sign,
            digits,
            self.exponent
        )

    def negate(self):
        return Number(
            -self.sign,
            self.digits,
            self.exponent
        )

    def invert(self):
        assert not self.equal_number(ZERO)

        quotient = []
        exponent = self.digits_length
        dividend = pow(10, exponent)
        dividend_history = set()

        while dividend:
            delta_exponent = 0
            while dividend < self.digits:
                delta_exponent += 1
                dividend *= pow(10, 1)

            quotient.append(floor(dividend / self.digits))
            dividend -= quotient[-1] * self.digits
            exponent += delta_exponent

            if dividend not in dividend_history:
                dividend_history.add(dividend)
            else:
                return Fraction(self.sign, ONE, self)

        quotient = sum(digit * pow(10, i)
                       for i, digit in enumerate(reversed(quotient)))

        return Number(
            self.sign,
            quotient,
            -self.exponent - exponent
        )

    def equal_number(self, number: "Number"):
        if self.digits == 0 and number.digits == 0:
            return True

        minimum_exponent = min(self.exponent, number.exponent)

        self_digits = self.digits
        self_digits *= pow(10, self.exponent - minimum_exponent)

        number_digits = number.digits
        number_digits *= pow(10, number.exponent - minimum_exponent)

        return self.sign == number.sign and self_digits == number_digits

    def less_than_number(self, number: "Number"):
        raise NotImplementedError

        if self.equal(ZERO) and number.equal(ZERO):
            return False
            
        if self.sign < number.sign:
            return True

        if self.digits < number.digits and self.exponent < number.exponent:
            return True

    def greater_than_number(self, number: "Number"):
        return not self.less_than_number(number) and not self.equal(number)

    def add_number(self, number: "Number"):
        minimun_exponent = min(self.exponent, number.exponent)
        digits = (self.sign * self.digits * pow(10, (self.exponent - minimun_exponent))) + \
            (number.sign * number.digits *
             pow(10, number.exponent - minimun_exponent))
        sign = 1 if digits >= 0 else -1
        digits = abs(digits)

        return Number(
            sign,
            digits,
            minimun_exponent
        )

    def subtract_number(self, number: "Number"):
        return self.add(number.negate())

    def multiply_number(self, number: "Number"):
        return Number(
            self.sign * number.sign,
            self.digits * number.digits,
            self.exponent + number.exponent
        )

    def divide_number(self, number: "Number"):
        return self.multiply(number.invert())

    def modulus_number(self, number: "Number"):
        assert self.is_integer
        assert number.is_integer
        return number.subtract_number(number.divide_number(self).integer)

    def equal_fraction(self, fraction: "Fraction"):
        raise NotImplementedError

    def add_fraction(self, fraction: "Fraction"):
        return Fraction.from_number(self).add_fraction(fraction)

    def subtract_fraction(self, fraction: "Fraction"):
        return Fraction.from_number(self).subtract_fraction(fraction)

    def multiply_fraction(self, fraction: "Fraction"):
        return Fraction.from_number(self).multiply_fraction(fraction)

    def divide_fraction(self, fraction: "Fraction"):
        return Fraction.from_number(self).divide_fraction(fraction)

    def modulus_fraction(self, fraction: "Fraction"):
        number = Number.from_fraction(fraction)
        return self.modulus_number(fraction)

    def less_than_fraction(self, fraction: "Fraction"):
        raise NotImplementedError

    def greater_than_fraction(self, fraction: "Fraction"):
        raise NotImplementedError


ZERO = Number(1, 0, 0)
ONE = Number(1, 1, 0)


class Fraction(Atom):
    __sign: int
    __numerator: "Atom"
    __denominator: "Atom"

    def __init__(self, sign: int, numerator: "Atom", denominator: "Atom"):
        assert sign == 1 or sign == -1
        assert denominator != 0

        self.__sign = sign
        self.__numerator = numerator
        self.__denominator = denominator

    def __str__(self):
        return "(" + str(self.numerator) + ")/(" + str(self.denominator) + ")"

    @classmethod
    def from_number(cls, number: "Number"):
        return cls(1, number, ONE)

    @property
    def sign(self):
        return self.__sign

    @property
    def numerator(self):
        return self.__numerator

    @property
    def denominator(self):
        return self.__denominator

    def compute(self, n: int = 15):
        assert type(self.numerator) is Number
        assert type(self.denominator) is Number

        if self.numerator.equal(ZERO):
            return ZERO

        quotient = []
        exponent = self.numerator.digits_length - self.denominator.digits_length
        dividend = self.numerator.digits

        for i in range(n):
            delta_exponent = 0
            while dividend < self.denominator.digits:
                delta_exponent += 1
                dividend *= pow(10, 1)

            quotient.append(floor(dividend / self.denominator.digits))
            dividend -= quotient[-1] * self.denominator.digits
            exponent += delta_exponent

            if not dividend:
                break

        quotient = sum(digit * pow(10, i)
                       for i, digit in enumerate(reversed(quotient)))

        return Number(
            self.sign * self.numerator.sign * self.denominator.sign,
            quotient,
            -self.denominator.exponent - exponent
        )

    @property
    def integer(self, n: int = 15):
        return Number.from_fraction(self, n).integer

    @property
    def floating(self, n: int = 15):
        return Number.from_fraction(self, n).floating

    def negate(self):
        return Fraction(-self.sign, self.numerator, self.denominator)

    def invert(self):
        return Fraction(self.sign, self.denominator, self.numerator)

    def equal_number(self):
        raise NotImplementedError

    def less_than_number(self, number: "Number"):
        raise NotImplementedError

    def greater_than_number(self, number: "Number"):
        raise NotImplementedError

    def add_number(self, number: "Number"):
        return self.add_fraction(Fraction.from_number(number))

    def subtract_number(self, number: "Number"):
        return self.subtract_fraction(Fraction.from_number(number))

    def multiply_number(self, number: "Number"):
        return self.multiply_fraction(Fraction.from_number(number))

    def divide_number(self, number: "Number"):
        return self.divide_fraction(Fraction.from_number(number))

    def modulus_number(self, number: "number"):
        self_number = Number.from_fraction(self)

        assert self_number.is_integer

        return self_number.modulus_number(number)

    def equal_fraction(self, fraction: "Fraction"):
        if self.numerator.equal(ZERO) and fraction.numerator.equal(ZERO):
            return True
        return self.sign == fraction.sign and self.numerator.equal(fraction.numerator) and self.denominator.equal(fraction.denominator)

    def add_fraction(self):
        raise NotImplementedError

    def subtract_fraction(self, fraction: "Fraction"):
        return self.add_fraction(fraction.negate())

    def multiply_fraction(self, fraction: "Fraction"):
        return Fraction(
            self.sign * fraction.sign,
            self.numerator.multiply(self.denominator),
            self.denominator.multiply(self.denominator)
        )

    def divide_fraction(self, fraction: "Fraction"):
        return self.multiply_fraction(fraction.invert())

    def modulus_fraction(self, fraction: "Fraction"):
        self_number = Number.from_fraction(self)
        number = Number.from_fraction(fraction)
        
        assert self_number.is_integer

        return self_number.modulus_fraction(number)

    def less_than_fraction(self, fraction: "Fraction"):
        raise NotImplementedError

    def greater_than_fraction(self, fraction: "Fraction"):
        raise NotImplementedError

