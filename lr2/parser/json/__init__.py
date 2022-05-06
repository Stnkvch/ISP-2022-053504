import re
import sys
from typing import IO, Any
from lr2.parser import ISerializer

sys.path.append("/Users/denis/PycharmProjects/ISP-2022-053504/lr2")

NONE_STRING = "null"
TRUE_STRING = "true"
FALSE_STRING = "false"

MONITOR_SYMBOL = "\\"

REGEX_DELETING_PATTERN = r"^[\{\[]\n\t*|\t*[\}\]]$"


class JSON(ISerializer):
    def _serialize_object(self, obj: Any, tab_count=0) -> str:
        object_type = type(obj)

        if object_type is dict:
            return self.serialize_dict(obj, tab_count=tab_count)

        if object_type is list:
            return self.serialize_list(obj, tab_count=tab_count)

        if object_type is str:
            return '"' + obj.replace('"', f'{MONITOR_SYMBOL}"') + '"'

        if object_type in (int, float):
            return str(obj)

        if isinstance(obj, type(None)):
            return NONE_STRING

        if object_type is bool:
            return TRUE_STRING if obj else FALSE_STRING

        raise TypeError(f"Unknown type {object_type}")

    def serialize_dict(self, obj: dict, tab_count=0) -> str:
        result = ""

        tab = '\t' * tab_count

        for key, value in obj.items():
            result += f'{tab}"{key}": {self.serialize_object(value, tab_count=tab_count + 1)},\n'

        return "{\n" + result.rstrip(",\n") + "\n" + tab + "}"

    def serialize_list(self, obj: list, tab_count=0) -> str:
        result = ""

        tab = '\t' * tab_count

        for item in obj:
            result += f"{tab}{self.serialize_object(item, tab_count=tab_count + 1)},\n"

        return "[\n" + result.rstrip(",\n") + "\n" + tab + "]"

    @staticmethod
    def check_value_end(char: str, tmp: str) -> bool:
        return char == '"' and len(tmp) > 0 and tmp[-1] != MONITOR_SYMBOL

    def deserialize_object(self, string: str) -> Any:
        if string.startswith("{"):
            return self.deserialize_dict(string)

        if string.startswith("["):
            return self.deserialize_list(string)

        if string.startswith('"'):
            return string.strip('"').replace(f'{MONITOR_SYMBOL}', '')

        if string == NONE_STRING:
            return None

        if string == TRUE_STRING:
            return True

        if string == FALSE_STRING:
            return False

        if string.find(".") != -1:
            return float(string)

        return int(string)

    def deserialize_dict(self, string: str) -> dict:
        string = re.sub(REGEX_DELETING_PATTERN, "", string).strip()

        result = {}
        is_key = True
        key = None
        tmp = ""
        char_index = 0
        string_len = len(string)

        brace_count = 0
        bracket_count = 0

        while char_index < string_len:
            char = string[char_index]

            if is_key:
                if self.check_value_end(char, tmp):
                    key = tmp + char

                    tmp = ""
                    is_key = False
                    char_index += 1  # skip ":"

                else:
                    tmp += char

            else:
                if brace_count == bracket_count == 0 and (
                    (
                        tmp.lstrip().startswith('"') and
                        self.check_value_end(char, tmp)
                    ) or
                    (
                        not tmp.startswith('"') and
                        char == ','
                    )
                ):
                    tmp = tmp + char
                    result[self.deserialize_object(
                        key)] = self.deserialize_object(tmp.strip().rstrip(','))

                    tmp = ""
                    is_key = True
                    # find next key start index
                    char_index = string.find('"', char_index + 1) - 1

                    if char_index < 0:
                        break

                else:
                    if char == '{':
                        brace_count += 1
                    if char == '[':
                        bracket_count += 1
                    if char == ']':
                        bracket_count -= 1
                    if char == '}':
                        brace_count -= 1

                    tmp += char

            char_index += 1

        if tmp.strip() != "":
            result[self.deserialize_object(key)] = self.deserialize_object(tmp.strip())

        return result

    def deserialize_list(self, string: str) -> list:
        string = re.sub(REGEX_DELETING_PATTERN, "", string)

        result = []
        tmp = ""
        char_index = 0
        string_len = len(string)

        brace_count = 0
        bracket_count = 0

        while char_index < string_len:
            char = string[char_index]

            if brace_count == bracket_count == 0 and (
                (
                    tmp.startswith('"') and
                    self.check_value_end(char, tmp)
                ) or
                (
                    not tmp.startswith('"') and
                    char == ','
                )
            ):
                tmp = tmp + char
                result.append(self.deserialize_object(
                    tmp.strip().rstrip(',')))

                tmp = ""
                char_index = string.find(',', char_index)

                if char_index < 0:
                    break

            else:
                if char == '{':
                    brace_count += 1
                if char == '[':
                    bracket_count += 1
                if char == ']':
                    bracket_count -= 1
                if char == '}':
                    brace_count -= 1

                tmp += char

            char_index += 1

        if tmp.strip() != "":
            result.append(self.deserialize_object(tmp.strip().rstrip(',')))

        return result

    def dump(self, obj: Any, fp: IO) -> None:
        fp.write(self.serialize_object(obj))

    def dumps(self, obj: Any) -> str:
        return self.serialize_object(obj)

    def load(self, fp: IO) -> dict:
        return self.deserialize_object(fp.read())

    def loads(self, s: str) -> dict:
        return self.deserialize_object(s)
