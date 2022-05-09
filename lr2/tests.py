from lr2.parser import YAML
from lr2.parser import TOML
from lr2.parser import JSON
from lr2.parser import Serializer
from func_factorial import factorial
from classs import B
import unittest


def test(self, obj):
    serializer = Serializer(obj())

    func_data = serializer.dumps(factorial)
    class_data = serializer.dumps(B)

    func_result = serializer.loads(func_data)
    class_result = serializer.loads(class_data)

    t1 = class_result(1, 2)
    t2 = B(1, 2)

    self.assertEqual((func_result(5), t1.a, t1.b), (factorial(5), t2.a, t2.b))


class SerializerTest(unittest.TestCase):
    def test_json(self):
        test(self, JSON)

    def test_toml(self):
        test(self, TOML)

    def test_yaml(self):
        test(self, YAML)


if __name__ == "__main__":
    unittest.main()
