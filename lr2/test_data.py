def factorial(number):
    if number == 0 or number == 1:
        return 1
    return number * factorial(number - 1)


class A:
    def __init__(self, a):
        self.a = a


class B(A):
    def __init__(self, a, b):
        super().__init__(a)
        self.b = b

