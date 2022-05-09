import math
import unittest
from ..classs import B
from ..parser import JSON
from .serializer import Serializer
from ..function import func


class ParserTest(unittest.TestCase):

    def test_function(self):
        parser = Serializer(JSON(), func)
        self.assertEqual(parser.t(2), math.cos(2*10*22*3))

    def test_class(self):
        parser = Serializer(JSON(), B)

        t1 = B(1, 2)
        t2 = parser.t(1, 2)

        self.assertEqual((t1.a, t1.b), (t2.a, t1.b))

    def test_instance(self):
        inst = B(1, 2)

        parser = Serializer(JSON(), inst)

        inst = parser.t
        inst2 = B(1, 2)

        self.assertEqual((inst.a, inst.b,), (inst2.a, inst2.b))


if __name__ == "__main__":
    unittest.main()
