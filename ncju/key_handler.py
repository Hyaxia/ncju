import curses
from ncju.json_viewer import JsonViewer


def handle_key(key: int, viewer: JsonViewer) -> bool:
    """
    Handle key input and return True if the application should continue running.
    """
    if key == ord("q"):
        return False
    elif key == curses.KEY_UP or key == ord("k"):
        # Check if we have a count
        if hasattr(viewer, "count") and viewer.count > 0:
            for _ in range(viewer.count):
                viewer.move_up()
            viewer.count = 0
        else:
            viewer.move_up()
    elif key == curses.KEY_DOWN or key == ord("j"):
        # Check if we have a count
        if hasattr(viewer, "count") and viewer.count > 0:
            for _ in range(viewer.count):
                viewer.move_down()
            viewer.count = 0
        else:
            viewer.move_down()
    elif key >= ord("0") and key <= ord("9"):
        # Build up count for next motion
        if not hasattr(viewer, "count"):
            viewer.count = 0
        viewer.count = viewer.count * 10 + (key - ord("0"))
    elif key == 10 or key == ord("l") or key == ord("h"):  # Enter key
        viewer.toggle_expand()
        viewer.count = 0 if hasattr(viewer, "count") else 0

    return True
