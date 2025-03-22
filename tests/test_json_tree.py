import pytest
from utils import get_size_of_file
from json_tree import build_tree
import json


def test_nested_json():
    nested_json_path = "./tests/test_data/nested_json.json"
    nested_json_size = get_size_of_file(nested_json_path)
    assert nested_json_size == 86  # this is the current size of the file

    with open(nested_json_path) as f:
        simple_json = json.load(f)
    tree = build_tree(simple_json)
    sorted_tree = sorted(tree.children, key=lambda x: x.size, reverse=True)
    assert sorted_tree[0].key == "children"
    assert sorted_tree[0].size == 21
    assert sorted_tree[1].key == "city"
    assert sorted_tree[1].size == 12
    assert sorted_tree[2].key == "name"
    assert sorted_tree[2].size == 8
    assert sorted_tree[3].key == "age"
    assert sorted_tree[3].size == 5

    assert tree.size == 46  # size without indentation and special marks


@pytest.mark.parametrize(
    "json_input, expected_size",
    [
        ({}, 0),
        ({"key": "value"}, 8),
        ({"key": "value", "key2": "value2"}, 18),
        ({"key": "value", "key2": "value2", "key3": "value3"}, 28),
        ({"key": "value", "nested": {"key": "value", "number": 55}}, 30),
        ({"key": "value", "nested": {"key": "value", "number": 55, "bool": True}}, 38),
        ([{"key1": "value1"}, {"key2": "value2"}], 20),
        ({"k": True}, 5),
    ],
    ids=[
        "empty_dict",
        "single_key_value",
        "multiple_key_values",
        "multiple_key_values_2",
        "nested_dict",
        "dict_with_bools",
        "list_of_dicts",
        "dict_with_bool",
    ],
)
def test_sizes(json_input: dict, expected_size: int):
    tree = build_tree(json_input)
    assert tree.size == expected_size
