import yaml
import sys
from typing import IO
from lr2.parser import ISerializer

sys.path.insert(0, "/Users/denis/PycharmProjects/ISP-2022-053504/lr2")


class YAML(ISerializer):

    def dump(self, obj: dict, fp: IO) -> None:
        yaml.dump(obj, fp)

    def dumps(self, obj: dict) -> str:
        return yaml.dump(obj)

    def load(self, fp: IO) -> dict:
        return yaml.load(fp)

    def loads(self, s: str) -> dict:
        return yaml.load(s)
