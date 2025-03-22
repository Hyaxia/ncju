import curses
import json
import sys
import os
import argparse
from json_viewer import JsonViewer
from json_tree import Node


def format_size(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024
    return f"{size:.2f}TB"

def draw_ui(stdscr, viewer: JsonViewer):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    # Draw header
    header = "NCJU - JSON Usage Viewer"
    stdscr.addstr(0, 0, header[:width-1], curses.A_BOLD)
    
    # Draw nodes
    nodes = viewer.get_visible_nodes()
    visible_nodes = nodes[viewer.scroll_pos:viewer.scroll_pos + height - 2]
    
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
            line = line[:width - 1]
            
        # Draw line with selection highlight
        if node == viewer.current_node:
            stdscr.addstr(y, 0, line, curses.A_REVERSE)
        else:
            stdscr.addstr(y, 0, line)
    
    # Draw footer
    footer = "↑↓: Navigate | Enter: Expand/Collapse | q: Quit"
    stdscr.addstr(height-1, 0, footer[:width-1], curses.A_BOLD)
    
    stdscr.refresh()

def main():
    parser = argparse.ArgumentParser(description='NCJU - JSON Usage Viewer')
    parser.add_argument('file', help='JSON file to analyze')
    args = parser.parse_args()

    try:
        with open(args.file, 'r') as f:
            json_data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)

    viewer = JsonViewer(json_data)
    
    def main_loop(stdscr):
        curses.curs_set(0)  # Hide cursor
        while True:
            draw_ui(stdscr, viewer)
            key = stdscr.getch()
            
            if key == ord('q'):
                break
            elif key == curses.KEY_UP:
                viewer.move_up()
            elif key == curses.KEY_DOWN:
                viewer.move_down()
            elif key == 10:  # Enter key
                viewer.toggle_expand()

    try:
        curses.wrapper(main_loop)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
