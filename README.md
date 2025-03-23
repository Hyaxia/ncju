this project is inspired by:
```
ncdu (NCurses Disk Usage) is a disk utility for Unix systems. Its name refers to its similar purpose to the du utility, but ncdu uses a text-based user interface under the [n]curses programming library.
```

ncju, short for NCurses Json Usage, is a file utility for Unix systems.
Its purpose is to do that ncdu does for disks, but for json files.
Basically map all key-value paris and show how much memory each one takes.

-----------------------

turns out that in mac the files are saved with encoding of us-ascii.
this means that each character is 8 bytes.
however when we load the data into python with `with open` we load it as unicode and then
it varies how many bytes it takes.

if now I take a simple text file and add a `❤️` to it, on mac it will change the encoding from ascii
to utf-8 because ascii is not able to represent that symbol.

we must take into account the encoding of a file to calculate the size of each key-value.
if we take a key-value from ascii then its a different calculation than utf-8 (unicode with 8-bit bytes).

------------------

another thing to take into account, in the file system it takes into account all of the separators, the `"` signs,
the indentation and such, that I dont neccessarily take into account in my calculation.


-----

example:

for the json
```
{
    "name": "John",
    "age": 30,
    "city": "New York",
    "children": [
        {
            "name": "Jane",
            "age": 10
        }
    ]
}
```

the result is:

```
NCJU - JSON Usage Viewer
▼ None: 46.00B
    name: 8.00B
    age: 5.00B
    city: 12.00B
  ▼ children: 21.00B
    ▼ None: 13.00B
        name: 8.00B
        age: 5.00B
```

the way the size is calculated is:

- size of key and size of the value are combined
- indentation between keys and values is ignored
- `"`, `,` and `{}` marks that are part of the json encoding are ignored

-----------------


another thing to check is - how should I calculate the size of each value?
if for each value I convert it to string and then check the length, how much time will it take
for large jsons? if its not too much, it might be preferable because its the easiest way.

