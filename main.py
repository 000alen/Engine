from Engine.Atom import Atom, Number, Fraction, ONE, ZERO
# from Engine.Algorithm import GCD

def GCD(a, b):
    while not a.equal(b):
        if a.greater_than(b):
            a = a.subtract(b)
        else:
            b = b.subtract(a)
    return a


a = Number(1, 10, 0)
b = Number(1, 7, 0)

print(GCD(a, b))
