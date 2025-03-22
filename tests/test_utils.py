from utils import get_size_of_file


def test_size_of_file():
    simple_json_path = '/Users/maximvovshin/software/ncju/tests/test_data/simple_json.json'
    simple_json_size =  get_size_of_file(simple_json_path)
    assert simple_json_size == 37


