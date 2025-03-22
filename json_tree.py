from typing import Any, Union
from size_calculator import get_size_as_string_in_bytes


class Leaf:
    """
    Leaf is either a key-pair value or a value in a list.
    """

    def __init__(self, value: Any, key=None):
        self.value = value
        self.key = key or ""
        self.size = self._calculate_size()

    def _calculate_size(self):
        return get_size_as_string_in_bytes(self.value)


class Node:
    """
    Node is a dictionary or a list.
    """

    def __init__(self, key, is_root=False, should_calculate_key=True):
        self.key = key
        self.should_calculate_key = should_calculate_key
        self.children: list[Union[Node, Leaf]] = []
        self.parent: Node = None
        self.is_root = is_root or key is None
        self.size = 0
        self.expanded = False

    def _calculate_size(self):
        self.size = 0
        # Add sizes of all children
        for child in self.children:
            self.size += child.size
            # Add size of child's key if it's a leaf and should calculate key
            if isinstance(child, Leaf):
                self.size += get_size_as_string_in_bytes(child.key)

        return self.size

    def add_child(self, child: Union["Node", "Leaf"]):
        self.children.append(child)
        child.parent = self
        self._calculate_size()  # Recalculate total size including the new child


def build_tree(json_data: Any) -> Union[Node, Leaf]:
    def _iterate_json(data: Any, key=None, should_calculate_key=True) -> Union[Node, Leaf]:
        if isinstance(data, (str, int, float, bool, type(None))):
            return Leaf(data, key)
        elif isinstance(data, dict):
            node = Node(key, should_calculate_key)
            for key, value in data.items():
                child = _iterate_json(
                    value, key, should_calculate_key=True
                )  # dict keys are always strings so we calculate them
                node.add_child(child)
            return node
        elif isinstance(data, list):
            node = Node(key)
            for i, value in enumerate(data):
                child = _iterate_json(
                    value, str(i), should_calculate_key=False
                )  # list items don't have keys
                node.add_child(child)
            return node
        else:
            raise ValueError(f"Unsupported type: {type(data)}")

    return _iterate_json(json_data)
