import math

a = 5


def _t(arg):
    b = 2

    def _f(arg):
        c = 123
        return math.sin(arg * a * b * c)
    return _f(arg)
