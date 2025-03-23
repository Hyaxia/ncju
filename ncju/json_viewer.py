import sys
from typing import Dict, Any, List, Tuple, Union
from ncju.json_tree import build_tree, Node, Leaf


class JsonViewer:
    def __init__(self, json_data: Dict[str, Any]):
        self.root = build_tree(json_data)
        self.current_node = self.root
        self.scroll_pos = 0
        self.selected_index = 0
        self.visible_height = 0  # Will be updated by draw_ui

    def get_visible_nodes_sorted(self) -> List[Tuple[Union[Node, Leaf], int]]:
        def _get_nodes(
            node: Union[Node, Leaf], level: int
        ) -> List[Tuple[Union[Node, Leaf], int]]:
            nodes = [(node, level)]
            if isinstance(node, Node) and node.expanded:
                # Sort children by size before processing them
                sorted_children = sorted(
                    node.children, key=lambda x: x.size, reverse=True
                )
                # Get all children nodes recursively
                for child in sorted_children:
                    nodes.extend(_get_nodes(child, level + 1))
            return nodes

        # Get all nodes with proper hierarchy
        return _get_nodes(self.root, 0)

    def toggle_expand(self):
        if isinstance(self.current_node, Node) and self.current_node.children:
            self.current_node.expanded = not self.current_node.expanded

    def move_up(self):
        nodes = self.get_visible_nodes_sorted()
        current_idx = next(
            i for i, (node, _) in enumerate(nodes) if node == self.current_node
        )
        if current_idx > 0:
            new_idx = current_idx - 1
            # Update scroll position if we would go above visible area
            if new_idx < self.scroll_pos:
                self.scroll_pos = new_idx
            self.current_node = nodes[new_idx][0]
            self.selected_index = new_idx

    def move_down(self):
        nodes = self.get_visible_nodes_sorted()
        current_idx = next(
            i for i, (node, _) in enumerate(nodes) if node == self.current_node
        )
        if current_idx < len(nodes) - 1:
            new_idx = current_idx + 1
            # Update scroll position if we would go below visible area
            # Account for header (1 line) and footer (1 line)
            visible_bottom = self.scroll_pos + (self.visible_height - 2)
            if new_idx >= visible_bottom:
                # Keep the selected item visible by scrolling
                self.scroll_pos = new_idx - (
                    self.visible_height - 3
                )  # -3 to account for header, footer, and keeping one line below visible
            self.current_node = nodes[new_idx][0]
            self.selected_index = new_idx
