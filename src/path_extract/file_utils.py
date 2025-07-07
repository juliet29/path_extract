import polars as pl


from pathlib import Path


def read_csv(path: Path, file_name: str | None = None):
    if file_name:
        _path = path / file_name
    else:
        _path = path
    assert _path.exists(), f"{_path} does not exist!"
    return pl.read_csv(_path)


def read_json(path: Path, file_name: str | None = None):
    if file_name:
        _path = path / file_name
    else:
        _path = path
    assert _path.exists(), f"{_path} does not exist!"
    with open(_path, "r") as f:
        data = json.load(f)
        # print(data)
        return data
