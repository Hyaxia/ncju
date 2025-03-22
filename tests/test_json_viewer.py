import sys
import pytest
from typing import Any, Dict, List
from json_viewer import JsonViewer, JsonNode

def calculate_actual_size(obj: Any, seen=None) -> int:
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([calculate_actual_size(v, seen) for v in obj.values()])
        size += sum([calculate_actual_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += calculate_actual_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([calculate_actual_size(i, seen) for i in obj])
    return size


def test_simple_dict():
    """Test size calculation for simple types"""
    test_data = {
        "string": "hello",
        "integer": 42,
        "float": 3.14,
        "boolean": True,
        "none": None
    }
    
    viewer = JsonViewer(test_data)
    actual_size = calculate_actual_size(test_data)
    
    assert viewer.root.size == actual_size

def test_nested_dict():
    """Test size calculation for nested dictionaries"""
    test_data = {
        "outer": {
            "inner": {
                "value": 42
            }
        }
    }
    
    viewer = JsonViewer(test_data)
    actual_size = calculate_actual_size(test_data)
    
    assert viewer.root.size == actual_size

def test_list_with_dicts():
    """Test size calculation for lists containing dictionaries"""
    test_data = {
        "list": [
            {"key1": "value1"},
            {"key2": "value2"}
        ]
    }
    
    viewer = JsonViewer(test_data)
    actual_size = calculate_actual_size(test_data)
    
    assert viewer.root.size == actual_size

def test_complex_structure():
    """Test size calculation for a complex nested structure"""
    test_data = {
        "users": [
            {
                "id": 1,
                "name": "John",
                "address": {
                    "street": "123 Main St",
                    "city": "Boston"
                }
            },
            {
                "id": 2,
                "name": "Jane",
                "address": {
                    "street": "456 Oak Ave",
                    "city": "New York"
                }
            }
        ],
        "settings": {
            "theme": "dark",
            "notifications": True
        }
    }
    
    viewer = JsonViewer(test_data)
    actual_size = calculate_actual_size(test_data)
    
    assert viewer.root.size == actual_size

def test_empty_structures():
    """Test size calculation for empty structures"""
    test_data = {
        "empty_dict": {},
        "empty_list": [],
        "nested_empty": {
            "empty": {}
        }
    }
    
    viewer = JsonViewer(test_data)
    actual_size = calculate_actual_size(test_data)
    
    assert viewer.root.size == actual_size

def test_node_expansion():
    """Test that node expansion works correctly"""
    test_data = {
        "level1": {
            "level2": {
                "level3": "value"
            }
        }
    }
    
    viewer = JsonViewer(test_data)
    
    # Initially root should be visible
    visible_nodes = viewer.get_visible_nodes_sorted()
    assert len(visible_nodes) == 1
    
    # Expand root
    viewer.current_node = viewer.root
    viewer.toggle_expand()
    visible_nodes = viewer.get_visible_nodes_sorted()
    assert len(visible_nodes) == 2  # root + level1
    
    # Expand level1
    viewer.current_node = viewer.root.children[0]
    viewer.toggle_expand()
    visible_nodes = viewer.get_visible_nodes_sorted()
    assert len(visible_nodes) == 3  # root + level1 + level2

def test_navigation():
    """Test navigation between nodes"""
    test_data = {
        "first": "value1",
        "second": "value2",
        "third": "value3"
    }
    
    viewer = JsonViewer(test_data)
    viewer.current_node = viewer.root
    viewer.toggle_expand()
    
    # Move down
    viewer.move_down()
    assert viewer.current_node.key == "first"
    
    # Move down again
    viewer.move_down()
    assert viewer.current_node.key == "second"
    
    # Move up
    viewer.move_up()
    assert viewer.current_node.key == "first" 