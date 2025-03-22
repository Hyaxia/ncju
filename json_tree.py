from typing import Any, Union
from size_calculator import get_size_as_string_in_bytes


class Leaf:
    def __init__(self, value: Any, key=None):
        self.value = value
        self.key = key or ""
        self.size = self._calculate_size()

    def _calculate_size(self):
        return get_size_as_string_in_bytes(self.value) + get_size_as_string_in_bytes(
            self.key
        )


class Node:
    def __init__(self, key, is_root=False):
        self.key = key
        self.children: list[Node | Leaf] = []
        self.parent: Node = None
        self.is_root = is_root or key is None
        self.size = self._calculate_size()

    def _calculate_size(self):
        self.size = 0
        key_size = 0
        if not self.is_root:
            key_size = get_size_as_string_in_bytes(self.key)

        for child in self.children:
            self.size += child.size

        return self.size + key_size

    def add_child(self, child: Union["Node", "Leaf"]):
        self.children.append(child)
        child.parent = self
        self.size += child.size


def iterate_json(json_data: Any) -> Node:
    def _iterate_json(data: Any, key=None) -> Node | Leaf:
        if isinstance(data, (str, int, float, bool, type(None))):
            return Leaf(data, key)
        elif isinstance(data, dict):
            node = Node(key)
            for key, value in data.items():
                child = _iterate_json(value, key)
                node.add_child(child)
            return node
        elif isinstance(data, list):
            node = Node(key)
            for i, value in enumerate(data):
                child = _iterate_json(value)
                node.add_child(child)
            return node

    return _iterate_json(json_data)
