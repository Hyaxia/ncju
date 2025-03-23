# NCJU - NCurses JSON Usage Viewer

## Installation

To make the `ncju` command available globally:

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/ncju.git
    cd ncju
    ```

2. Create a symbolic link to make the command available globally:

    ```bash
    sudo ln -s "$(pwd)/ncju" /usr/local/bin/ncju
    ```

    If you're on macOS and don't have write permissions to `/usr/local/bin`, you can use:

    ```bash
    ln -s "$(pwd)/ncju" ~/.local/bin/ncju
    ```

    (Make sure `~/.local/bin` is in your PATH)

3. Update `ncju` with the path to the cloned repo

Now you can use the `ncju` command from anywhere on your system!

this project is inspired by:

```
ncdu (NCurses Disk Usage) is a disk utility for Unix systems. Its name refers to its similar purpose to the du utility, but ncdu uses a text-based user interface under the [n]curses programming library.
```

ncju, short for NCurses Json Usage, is a file utility for Unix systems.
Its purpose is to do that ncdu does for disks, but for json files.
Basically map all key-value paris and show how much memory each one takes.

---
## Size Calculation Details

The way the size calculation in `ncju` is made is by encoding the string into a utf-8 string and calculating the size.
For additional info refer to `get_size_as_string_in_bytes`.

### Understanding Size Differences
- The size shown by `ncju` may differ from the file size on disk because:
  - JSON files on disk include formatting characters (spaces, newlines)
  - Text encodings can vary between disk and memory (we use utf-8 for calculation)
  - `ncju` only measures the actual data content size

### Size Calculation in ncju
- Measures only the raw data content
- Uses UTF-8 encoding consistently for all strings