from ncju.size_calculator import get_size_as_string_in_bytes


def test_get_size_in_bytes():
    with open("/Users/maximvovshin/software/ncju/tests/test_data/simple_list") as f:
        simple_list = f.read()
    assert get_size_as_string_in_bytes("hello") == 5
    assert get_size_as_string_in_bytes(42) == 2
    assert get_size_as_string_in_bytes(3.14) == 4
    assert get_size_as_string_in_bytes([12, 342, 5, 23]) == 16
    assert get_size_as_string_in_bytes(simple_list) == 16
    assert get_size_as_string_in_bytes("你好") == 6
    assert get_size_as_string_in_bytes("👋") == 4
    assert get_size_as_string_in_bytes("👋👋") == 8
