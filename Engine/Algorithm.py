def GCD(a: "Atom", b: "Atom"):
    wrapper = {
        (Number, Number): GCD_number,
        (Fraction, Fraction): GCD_fraction,
        (Number, Fraction): GCD_number_fraction
    }
    return wrapper[type(a), type(b)](a, b)


def GCD_number(a: "Number", b: "Number"):
    assert a.is_integer
    assert b.is_integer




def GCD_fraction(a: "Fraction", b: "Fraction"):
    pass


def GCD_number_fraction(a: "Number", b: "Fraction"):
    pass


from Engine.Atom import Atom, Number, Fraction
