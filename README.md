# NCJU - NCurses JSON Usage Viewer

Easily identify large areas of a json file!

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
The following json:
```
{"name": "John","age": 30,"city": "New York","children": [{"name": "Jane","age": 10}]}
```

becomes:
```
NCJU - JSON Usage Viewer
▼ [ROOT]: 90.00B
  ▼ children: 29.00B
    ▼ 0: 27.00B
        name: 4.00B
        age: 2.00B
    city: 8.00B
    name: 4.00B
    age: 2.00B
```
---
The following json
```
[
    {
        "key1": "value1",
        "k": true
    },
    {
        "key2": "value2"
    }
]
```

becomes:
```
NCJU - JSON Usage Viewer
▼ [ROOT]: 51.00B
  ▼ 0: 29.00B
      key1: 6.00B
      k: 4.00B
  ▼ 1: 18.00B
      key2: 6.00B
```