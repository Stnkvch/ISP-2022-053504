import math
import unittest
import sys
from ..test_data import B
from lr2.parser.json import JSON
from .__init__ import Serializer
from ..test_module import _t


sys.path.append(".")
sys.path.append("..")


class ParserTest(unittest.TestCase):

    def test_function(self):
        parser = Serializer(JSON(), _t)
        self.assertEqual(parser.t(2), math.sin(2*123*2*5))

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
