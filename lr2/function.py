import math

NUM1 = 10


def func(value):
    num2 = 22

    def _f(value):
        num3 = 3
        return math.cos(value * NUM1 * num2 * num3)
    return _f(value)
