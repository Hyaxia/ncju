# NCJU - NCurses JSON Usage Viewer

`ncju`, short for NCurses Json Usage, is a file utility for Unix systems.
Its purpose is to do what ncdu does for disks, but for json files.
Basically map all key-value paris and show how much memory each one takes.

## Installation

1. `brew tap Hyaxia/ncju`
2. `brew install ncju`
3. enjoy :)

## Usage:

1. Run `ncju <json-file>` to analyze a JSON file
2. Navigate using:
   - Arrow keys (↑/↓) or (k/h) to move up/down
   - Enter/l/h/Right arrow (→) to expand a node
   - l/h/Left arrow (←) to collapse a node
   - q to quit

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
The following json - https://microsoftedge.github.io/Demos/json-dummy-data/5MB.json
becomes:
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
