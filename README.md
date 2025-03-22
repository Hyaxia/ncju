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




