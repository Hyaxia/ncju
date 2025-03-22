import curses
import json
import sys
import argparse
from json_viewer import JsonViewer
from ui_drawer import draw_ui
from key_handler import handle_key


def main():
    parser = argparse.ArgumentParser(description="NCJU - JSON Usage Viewer")
    parser.add_argument("file", help="JSON file to analyze")
    args = parser.parse_args()

    try:
        with open(args.file, "r") as f:
            json_data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)

    viewer = JsonViewer(json_data)

    def main_loop(stdscr):
        curses.curs_set(0)  # Hide cursor
        running = True
        while running:
            draw_ui(stdscr, viewer)
            key = stdscr.getch()
            running = handle_key(key, viewer)

    try:
        curses.wrapper(main_loop)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
