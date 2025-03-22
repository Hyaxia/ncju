from utils import get_size_of_file
from json_tree import iterate_json
import json


def test_iterate_json():
    simple_json_path = '/Users/maximvovshin/software/ncju/tests/test_data/simple_json.json'
    simple_json_size =  get_size_of_file(simple_json_path)
    assert simple_json_size == 37

    with open(simple_json_path) as f:
        simple_json = json.load(f)
    tree = iterate_json(simple_json)
    assert tree.size == simple_json_size


