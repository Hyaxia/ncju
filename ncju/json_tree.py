from typing import Any, Union
from ncju.size_calculator import get_size_as_string_in_bytes


class Leaf:
    """
    Leaf is a "simple" value in a dictionary or a list.
    """

    def __init__(self, data: Any, key=None):
        self.data = data
        self.key = key or ""
        self.size = get_size_as_string_in_bytes(self.data)


class Node:
    """
    Node is a dictionary or a list.
    """

    def __init__(self, key, is_root=False, data=None):
        self.key = key
        self.data = data
        self.children: list[Union[Node, Leaf]] = []
        self.parent: Node = None
        self.is_root = is_root or key is None
        self.size = get_size_as_string_in_bytes(self.data)
        self.expanded = False

    def add_child(self, child: Union["Node", "Leaf"]):
        self.children.append(child)
        child.parent = self


def build_tree(json_data: Any) -> Union[Node, Leaf]:
    def _iterate_json(data: Any, key=None) -> Union[Node, Leaf]:
        if isinstance(data, (str, int, float, bool, type(None))):
            return Leaf(data=data, key=key)
        elif isinstance(data, dict):
            node = Node(key=key, data=data)
            for key, value in data.items():
                child = _iterate_json(
                    value, key
                )  # dict keys are always strings so we calculate them
                node.add_child(child)
            return node
        elif isinstance(data, list):
            node = Node(key=key, data=data)
            for i, value in enumerate(data):
                child = _iterate_json(value, str(i))  # list items don't have keys
                node.add_child(child)
            return node
        else:
            raise ValueError(f"Unsupported type: {type(data)}")

    root = _iterate_json(json_data)
    root.key = "[ROOT]"
    return root
