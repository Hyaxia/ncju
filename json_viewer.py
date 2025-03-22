import sys
from typing import Dict, Any, List, Tuple

class JsonNode:
    def __init__(self, key: str, value: Any, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.children: List[JsonNode] = []
        self.expanded = False
        self.size = self._calculate_size()

    def _calculate_size(self) -> int:
        """Calculate the total size of the node including its key and value."""
        if self.key != "root":
            key_size = sys.getsizeof(self.key)
        else:
            key_size = 0
        if isinstance(self.value, (str, int, float, bool, type(None))):
            return key_size + sys.getsizeof(self.value)
        elif isinstance(self.value, (list, dict)):
            # Add up sizes of all children plus the container itself
            container_size = sys.getsizeof(self.value)
            children_size = sum(child.size for child in self.children)
            return key_size + container_size + children_size
        return key_size

    def add_child(self, child: 'JsonNode'):
        self.children.append(child)
        child.parent = self
        # Recalculate size after adding a child
        self.size = self._calculate_size()
        # Update parent sizes up the tree
        current = self.parent
        while current:
            current.size = current._calculate_size()
            current = current.parent

class JsonViewer:
    def __init__(self, json_data: Dict[str, Any]):
        self.root = JsonNode("root", json_data)
        self.current_node = self.root
        self.scroll_pos = 0
        self.selected_index = 0
        self._build_tree(self.root)

    def _build_tree(self, node: JsonNode):
        """
        Builds the tree of JsonNode objects from the ground up.
        """
        if isinstance(node.value, (str, int, float, bool, type(None))):
            return node
        elif isinstance(node.value, dict):
            for key, value in node.value.items():
                child = self._build_tree(JsonNode(key, value))
                node.add_child(child)
            return node
        elif isinstance(node.value, list):
            for i, value in enumerate(node.value):
                child = self._build_tree(JsonNode(f"[{i}]", value))
                node.add_child(child)
            return node
        else:
            raise ValueError(f"Unsupported value type: {type(node.value)}")

    def get_visible_nodes(self) -> List[Tuple[JsonNode, int]]:
        def _get_nodes(node: JsonNode, level: int) -> List[Tuple[JsonNode, int]]:
            nodes = [(node, level)]
            if node.expanded:
                for child in node.children:
                    nodes.extend(_get_nodes(child, level + 1))
            return nodes
        return _get_nodes(self.root, 0)

    def toggle_expand(self):
        if self.current_node.children:
            self.current_node.expanded = not self.current_node.expanded

    def move_up(self):
        nodes = self.get_visible_nodes()
        current_idx = next(i for i, (node, _) in enumerate(nodes) if node == self.current_node)
        if current_idx > 0:
            self.current_node = nodes[current_idx - 1][0]
            self.selected_index = current_idx - 1

    def move_down(self):
        nodes = self.get_visible_nodes()
        current_idx = next(i for i, (node, _) in enumerate(nodes) if node == self.current_node)
        if current_idx < len(nodes) - 1:
            self.current_node = nodes[current_idx + 1][0]
            self.selected_index = current_idx + 1 