# NCJU - NCurses JSON Usage Viewer

## Installation

1. `brew tap Hyaxia/ncju`
2. `brew install ncju`
3. enjoy :)

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


### UI Preview
```
NCJU - JSON Usage Viewer
▼ [ROOT]: 4.50MB
  ▶ 181: 484.00B
  ▶ 378: 484.00B
  ▶ 575: 484.00B
  ▶ 772: 484.00B
  ▶ 973: 484.00B
  ▶ 1170: 484.00B
  ▶ 1367: 484.00B
  ▶ 1564: 484.00B
  ▶ 1765: 484.00B
  ▶ 1962: 484.00B
  ▶ 2159: 484.00B
  ▶ 2356: 484.00B
  ▶ 2557: 484.00B
  ▶ 2754: 484.00B
  ▶ 2951: 484.00B
  ▶ 3148: 484.00B
  ▶ 3349: 484.00B
```
