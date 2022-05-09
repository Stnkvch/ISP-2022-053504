import argparse
import re
from lr2.parser import Serializer, ISerializer
from lr2.parser import JSON
from lr2.parser import TOML
from lr2.parser import YAML


def get_serializer(string: str) -> ISerializer:
    if string == "json":
        return JSON

    if string == "toml":
        return TOML

    if string == "yaml":
        return YAML

    raise TypeError("Error")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("source", type=str, help="Path to source file")
    parser.add_argument("format", type=str, help="Serialize format(json, toml or yaml) for result")
    parser.add_argument("-r", "--result-file", type=str, help="Path to result file. If not exist, it will be created")

    args = parser.parse_args()

    result_format = args.format

    source_path = args.source
    source_format = re.search(r"\w+$", source_path).group()

    if source_format == result_format:
        print("Same type")
        exit()

    source_serializer = Serializer(get_serializer(source_format))
    result_serializer = Serializer(get_serializer(result_format))

    with open(source_path) as file:
        obj = source_serializer.load(file)

        if args.result_file is not None:
            with open(args.result_file, "w") as output_file:
                result_serializer.dump(obj, output_file)
        else:
            print(result_serializer.dumps(obj))
