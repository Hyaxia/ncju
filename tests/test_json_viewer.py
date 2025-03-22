from json_viewer import JsonViewer

test_json = {
    "name": "John",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "country": "USA"
    },
    "hobbies": ["reading", "gaming", "coding"]
}

def test_json_viewer_init():
    viewer = JsonViewer(test_json)
    assert viewer.root is not None
    assert viewer.current_node == viewer.root
    assert viewer.scroll_pos == 0
    assert viewer.selected_index == 0

def test_get_visible_nodes_sorted():
    viewer = JsonViewer(test_json)
    nodes = viewer.get_visible_nodes_sorted()
    
    # Initially only root node should be visible since nothing is expanded
    assert len(nodes) == 1
    assert nodes[0][0] == viewer.root
    assert nodes[0][1] == 0  # Root level is 0
    
    # Expand root node
    viewer.root.expanded = True
    nodes = viewer.get_visible_nodes_sorted()
    
    # Should now see root + its immediate children
    assert len(nodes) > 1
    # Nodes should be sorted by size in descending order
    sizes = [node[0].size for node in nodes[1:]]  # Skip root node
    assert sizes == sorted(sizes, reverse=True)

def test_toggle_expand():
    viewer = JsonViewer(test_json)
    
    # Initially not expanded
    assert not viewer.root.expanded
    
    # Toggle expand
    viewer.toggle_expand()
    assert viewer.root.expanded
    
    # Toggle collapse
    viewer.toggle_expand()
    assert not viewer.root.expanded

def test_move_up_down():
    viewer = JsonViewer(test_json)
    viewer.root.expanded = True
    
    initial_node = viewer.current_node
    
    # Move down
    viewer.move_down()
    assert viewer.current_node != initial_node
    assert viewer.selected_index == 1
    
    # Move back up
    viewer.move_up()
    assert viewer.current_node == initial_node
    assert viewer.selected_index == 0
    
    # Try moving up when at top (should stay at top)
    viewer.move_up()
    assert viewer.current_node == initial_node
    assert viewer.selected_index == 0
