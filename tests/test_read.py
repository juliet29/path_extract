from path_extract.paths import PATH_TO_INPUTS
from path_extract.clmt_pilot.study import read_json


def test_read_dample_json():
    expected_result = {"index": "0", "project": "p1_pier6", "experiment": "exp_0"}
    result = read_json(PATH_TO_INPUTS, "sample.json")
    assert result == expected_result
    
