from Engine.Atom import Atom, Number, Fraction, ONE, ZERO

print(
    Fraction(1, ZERO, ONE).equal(Fraction(1, ZERO, Number(1, 2, 0)))
)
