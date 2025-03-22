from utils import get_size_of_file
from json_tree import build_tree
import json


def test_iterate_json():
    simple_json_path = './tests/test_data/simple_json.json'
    simple_json_size =  get_size_of_file(simple_json_path)
    assert simple_json_size == 37

    with open(simple_json_path) as f:
        simple_json = json.load(f)
    tree = build_tree(simple_json)
    assert tree.size == simple_json_size


def test_nested_json():
    nested_json_path = './tests/test_data/nested_json.json'
    nested_json_size =  get_size_of_file(nested_json_path)
    assert nested_json_size == 86  # this is the current size of the file

    with open(nested_json_path) as f:
        simple_json = json.load(f)
    tree = build_tree(simple_json)
    assert tree.size == 47  # size without indentation and special marks

NCJU - JSON Usage Viewer
▼ None: 47.00B
  ▼ children: 22.00B
    ▼ 0: 14.00B
        name: 8.00B
        age: 5.00B
    city: 12.00B
    name: 8.00B
    age: 5.00B