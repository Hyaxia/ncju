from json_viewer import JsonViewer
from json_tree import Node, Leaf

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

def test_list_items():
    list_json = {
        "items": [
            {"name": "Item 1", "value": 100},
            {"name": "Item 2", "value": 200}
        ]
    }
    viewer = JsonViewer(list_json)
    viewer.root.expanded = True
    viewer.root.children[0].expanded = True  # Expand the items list
    
    nodes = viewer.get_visible_nodes_sorted()
    # Verify list items have proper keys
    assert any(node[0].key == "0" for node in nodes)
    assert any(node[0].key == "1" for node in nodes)

def test_sorting_with_list():
    # Test data similar to myjsontest.json
    test_data = {
        "name": "John",
        "age": 30,
        "city": "New York",
        "children": [
            {
                "name": "Jane",
                "age": 10
            }
        ]
    }
    
    viewer = JsonViewer(test_data)
    
    # Initially only root should be visible
    nodes = viewer.get_visible_nodes_sorted()
    assert len(nodes) == 1
    root_node, root_level = nodes[0]
    assert root_level == 0
    assert root_node.size > 0  # Root should have size
    
    # Expand root
    viewer.root.expanded = True
    nodes = viewer.get_visible_nodes_sorted()
    
    # Check first level sorting (children, city, name, age)
    first_level_nodes = [(node.key, node.size) for node, level in nodes if level == 1]
    assert [node[0] for node in first_level_nodes] == ["children", "city", "name", "age"]
    
    # Verify sizes are in descending order
    sizes = [node[1] for node in first_level_nodes]
    assert sizes == sorted(sizes, reverse=True)
    
    # Find children node and expand it
    children_node = next(node for node, level in nodes if node.key == "children")
    children_node.expanded = True
    nodes = viewer.get_visible_nodes_sorted()
    
    # Check that list item "0" appears under children
    children_level = next(level for node, level in nodes if node.key == "children")
    list_items = [(node.key, level) for node, level in nodes if level == children_level + 1]
    assert len(list_items) == 1
    assert list_items[0][0] == "0"  # First item should be "0"
    
    # Expand list item "0"
    list_node = next(node for node, level in nodes if node.key == "0")
    list_node.expanded = True
    nodes = viewer.get_visible_nodes_sorted()
    
    # Check sorting of items within list item (name, age)
    list_level = next(level for node, level in nodes if node.key == "0")
    list_contents = [(node.key, node.size) for node, level in nodes if level == list_level + 1]
    assert [item[0] for item in list_contents] == ["name", "age"]
    assert list_contents[0][1] > list_contents[1][1]  # name should be bigger than age
