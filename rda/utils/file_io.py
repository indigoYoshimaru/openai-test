from typing import Text, Union, List, Dict


def read_json(file_path: Text) -> Union[List, Dict]:
    import json

    with open(file_path) as f:
        output = json.load(f)
    return output


def read_yaml(file_path: Text) -> Union[List, Dict]:
    import yaml

    with open(file_path) as f:
        output = yaml.full_load(f)
    return output
