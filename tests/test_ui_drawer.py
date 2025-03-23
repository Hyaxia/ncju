import pytest
from ncju.ui_drawer import format_size, draw_ui
from ncju.json_viewer import JsonViewer
import json


class MockCursesWindow:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.lines = [[" " for _ in range(width)] for _ in range(height)]
        self.attributes = [[0 for _ in range(width)] for _ in range(height)]

    def getmaxyx(self):
        return self.height, self.width

    def clear(self):
        self.lines = [[" " for _ in range(self.width)] for _ in range(self.height)]
        self.attributes = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def addstr(self, y, x, text, attr=0):
        if y >= self.height or x >= self.width:
            return
        text = text[: self.width - x]
        for i, char in enumerate(text):
            if x + i < self.width:
                self.lines[y][x + i] = char
                self.attributes[y][x + i] = attr

    def refresh(self):
        pass

    def get_content(self):
        return ["".join(line).rstrip() for line in self.lines]


def test_format_size():
    assert format_size(0) == "0.00B"
    assert format_size(1024) == "1.00KB"
    assert format_size(1024 * 1024) == "1.00MB"
    assert format_size(1024 * 1024 * 1024) == "1.00GB"
    assert format_size(500) == "500.00B"
    assert format_size(1500) == "1.46KB"
    assert format_size(1500000) == "1.43MB"
    assert format_size(1500000000) == "1.40GB"


def test_draw_ui_with_nested_json():
    # Load test data
    with open("./tests/test_data/nested_json.json") as f:
        test_json = json.load(f)

    viewer = JsonViewer(test_json)

    # Create a mock curses window
    mock_stdscr = MockCursesWindow(20, 80)

    # Test drawing UI
    draw_ui(mock_stdscr, viewer)

    # Get the content of the window
    content = mock_stdscr.get_content()

    # Verify header
    assert "NCJU - JSON Usage Viewer" in content[0]

    # Verify footer
    assert "↑↓/kj: Navigate | Enter/h/l: Expand/Collapse | q: Quit" in content[-1]

    assert "▶ [ROOT]" in content[1]

    # expand root node
    viewer.root.expanded = True
    draw_ui(mock_stdscr, viewer)
    content = mock_stdscr.get_content()

    # Verify content
    assert "▼ [ROOT]" in content[1]
    assert "children:" in content[2]  # First visible node
    assert "city:" in content[3]  # Second visible node
    assert "name:" in content[4]  # Third visible node
    assert "age:" in content[5]  # Fourth visible node


def test_draw_ui_with_simple_json():
    # Load test data
    with open("./tests/test_data/simple_json.json") as f:
        test_json = json.load(f)

    viewer = JsonViewer(test_json)

    # Create a mock curses window
    mock_stdscr = MockCursesWindow(10, 40)  # Smaller window size

    # Test drawing UI
    draw_ui(mock_stdscr, viewer)

    # Get the content of the window
    content = mock_stdscr.get_content()

    # Verify header
    assert "NCJU - JSON Usage Viewer" in content[0]

    # Verify footer
    assert "↑↓/kj: Navigate | Enter/h/l: Expand" in content[-1]


def test_scrolling_behavior():
    # Create a large test JSON with many items
    test_json = {
        "items": [{"id": str(i), "value": "x" * 100} for i in range(50)]  # 50 items
    }
    viewer = JsonViewer(test_json)

    # Create a small window to force scrolling
    mock_stdscr = MockCursesWindow(
        10, 80
    )  # Only 8 lines visible (10 - 2 for header/footer)

    # Expand root node to show all items
    viewer.root.expanded = True
    viewer.root.children[0].expanded = True  # Expand the items array

    # Test initial state
    draw_ui(mock_stdscr, viewer)
    content = mock_stdscr.get_content()
    assert "▼ [ROOT]" in content[1]
    assert "items:" in content[2]

    # Test moving down
    for _ in range(5):  # Move down 5 times
        viewer.move_down()
        draw_ui(mock_stdscr, viewer)
        content = mock_stdscr.get_content()
        # Verify the selected item is always visible
        assert any(
            "▶" in line or "▼" in line for line in content[1:-1]
        )  # Exclude header and footer
        # Verify the highlighted line is visible
        highlighted_line = next(
            i for i, line in enumerate(content[1:-1]) if "▶" in line or "▼" in line
        )
        assert 0 <= highlighted_line < len(content[1:-1])

    # Test moving up
    for _ in range(5):  # Move up 5 times
        viewer.move_up()
        draw_ui(mock_stdscr, viewer)
        content = mock_stdscr.get_content()
        # Verify the selected item is always visible
        assert any(
            "▶" in line or "▼" in line for line in content[1:-1]
        )  # Exclude header and footer
        # Verify the highlighted line is visible
        highlighted_line = next(
            i for i, line in enumerate(content[1:-1]) if "▶" in line or "▼" in line
        )
        assert 0 <= highlighted_line < len(content[1:-1])

    # Test moving to the bottom
    while viewer.selected_index < len(viewer.get_visible_nodes_sorted()) - 1:
        viewer.move_down()
        draw_ui(mock_stdscr, viewer)
        content = mock_stdscr.get_content()
        # Verify the selected item is always visible
        assert any(
            "▶" in line or "▼" in line for line in content[1:-1]
        )  # Exclude header and footer
        # Verify the highlighted line is visible
        highlighted_line = next(
            i for i, line in enumerate(content[1:-1]) if "▶" in line or "▼" in line
        )
        assert 0 <= highlighted_line < len(content[1:-1])

    # Test moving to the top
    while viewer.selected_index > 0:
        viewer.move_up()
        draw_ui(mock_stdscr, viewer)
        content = mock_stdscr.get_content()
        # Verify the selected item is always visible
        assert any(
            "▶" in line or "▼" in line for line in content[1:-1]
        )  # Exclude header and footer
        # Verify the highlighted line is visible
        highlighted_line = next(
            i for i, line in enumerate(content[1:-1]) if "▶" in line or "▼" in line
        )
        assert 0 <= highlighted_line < len(content[1:-1])
