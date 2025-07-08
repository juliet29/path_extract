from pathlib import Path


def get_path_subdirectories(path: Path):
    return [i for i in path.iterdir() if i.is_dir] 