import yaml
from typing import IO, Any
from ..serializer import ISerializer


class YAML(ISerializer):

    def dump(self, obj: Any, fp: IO) -> None:
        yaml.dump(obj, fp)

    def dumps(self, obj: Any) -> str:
        return yaml.dump(obj)

    def load(self, fp: IO) -> Any:
        return yaml.load(fp)

    def loads(self, s: str) -> Any:
        return yaml.load(s)
