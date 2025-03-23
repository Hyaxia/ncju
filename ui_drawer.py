import curses
from json_viewer import JsonViewer
from json_tree import Node


def format_size(size: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024
    return f"{size:.2f}TB"


def draw_ui(stdscr, viewer: JsonViewer):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    viewer.visible_height = height  # Update visible height for scrolling

    # Draw header
    header = "NCJU - JSON Usage Viewer"
    stdscr.addstr(0, 0, header[: width - 1], curses.A_BOLD)

    # Draw nodes
    nodes = viewer.get_visible_nodes_sorted()
    visible_nodes = nodes[viewer.scroll_pos : viewer.scroll_pos + height - 2]

    for i, (node, level) in enumerate(visible_nodes):
        if i >= height - 2:
            break

        y = i + 1
        if y >= height:
            break

        # Calculate prefix
        prefix = "  " * level
        if isinstance(node, Node) and node.children:
            prefix += "▶ " if not node.expanded else "▼ "
        else:
            prefix += "  "

        # Format line
        line = f"{prefix}{node.key}: {format_size(node.size)}"
        if len(line) > width - 1:
            line = line[: width - 1]

        # Draw line with selection highlight
        if node == viewer.current_node:
            stdscr.addstr(y, 0, line, curses.A_REVERSE)
        else:
            stdscr.addstr(y, 0, line)

    # Draw footer
    footer = "↑↓/kj: Navigate | Enter/h/l: Expand/Collapse | q: Quit"
    stdscr.addstr(height - 1, 0, footer[: width - 1], curses.A_BOLD)

    stdscr.refresh()
