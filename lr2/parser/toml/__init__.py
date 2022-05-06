import toml
from typing import IO, Any
from lr2.parser import ISerializer
from lr2.parser.const import STRING_TO_OBJECT_DICT, OBJECT_TO_STRING_DICT


class TOML(ISerializer):

    def adapt_object_dict(self, obj: Any) -> Any:
        object_type = type(obj)

        if object_type is dict:
            result = {}

            for key, value in obj.items():
                result[key] = self.adapt_object_dict(value)

            return result

        elif object_type is list:
            return [self.adapt_object_dict(item) for item in obj]

        elif object_type in OBJECT_TO_STRING_DICT:
            return {
                OBJECT_TO_STRING_DICT[object_type]: str(obj)
            }
        elif isinstance(obj, type(None)):
            return {
                "None": "None"
            }

    def restore_object_dict(self, obj: Any) -> Any:
        object_type = type(obj)

        if object_type is dict:
            if len(obj.keys()) == 1:
                key, value = list(obj.items())[0]

                if key == "None":
                    return None
                elif key in STRING_TO_OBJECT_DICT:
                    return STRING_TO_OBJECT_DICT[key](value)

            result = {}
            for key, value in obj.items():
                result[key] = self.restore_object_dict(value)

            return result
        else:
            return [self.restore_object_dict(item) for item in obj]

    def dump(self, obj: dict, fp: IO) -> None:
        toml.dump(self.adapt_object_dict(obj), fp)

    def dumps(self, obj: dict) -> str:
        return toml.dumps(self.adapt_object_dict(obj))

    def load(self, fp: IO) -> dict:
        return self.restore_object_dict(toml.load(fp))

    def loads(self, s: str) -> dict:
        return self.restore_object_dict(toml.loads(s))
