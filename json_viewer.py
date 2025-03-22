import sys
from typing import Dict, Any, List, Tuple
from json_tree import build_tree, Node, Leaf

class JsonViewer:
    def __init__(self, json_data: Dict[str, Any]):
        self.root = build_tree(json_data)
        self.current_node = self.root
        self.scroll_pos = 0
        self.selected_index = 0

    def get_visible_nodes(self) -> List[Tuple[Node | Leaf, int]]:
        def _get_nodes(node: Node | Leaf, level: int) -> List[Tuple[Node | Leaf, int]]:
            nodes = [(node, level)]
            if isinstance(node, Node) and node.expanded:
                # Get all children nodes recursively
                child_nodes = []
                for child in node.children:
                    child_nodes.extend(_get_nodes(child, level + 1))
                # Sort children by size before adding to nodes
                child_nodes.sort(key=lambda x: x[0].size, reverse=True)
                nodes.extend(child_nodes)
            return nodes
        return _get_nodes(self.root, 0)

    def toggle_expand(self):
        if isinstance(self.current_node, Node) and self.current_node.children:
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