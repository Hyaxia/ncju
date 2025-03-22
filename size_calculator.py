from typing import Any


def get_size_as_string_in_bytes(data: str) -> int:
    """
    Calculate size of simple data types

    For strings the size is calculated in bytes using utf8 encoding
    """
    string_data = str(data)
    return len(string_data.encode("utf8"))

