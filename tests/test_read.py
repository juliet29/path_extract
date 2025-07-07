from path_extract.paths import PATH_TO_INPUTS, PATH_TO_CLMT_PROJECTS
from path_extract.file_utils import read_json


def test_read_sample_json():
    expected_result = {"index": "0", "project": "p1_pier6", "experiment": "exp_0"}
    result = read_json(PATH_TO_INPUTS, "sample.json")
    assert result == expected_result


def test_read_pier6():
    expected_result = {
        "index": 0,
        "project": "Pier 6",
        "experiment": "EDC original scope",
    }
    result = read_json(PATH_TO_CLMT_PROJECTS, "pier_6/exp_0/info.json")
    assert result == expected_result


# C:\Users\juliet.intern\_SCAPECode\pathfinder\inputs\250701_CLMT_Pilot_Sprint\pier_6\exp_0\info.json
