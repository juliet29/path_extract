from pathlib import Path
from typing import Iterable, TypeVar
from itertools import chain

T = TypeVar("T")


def get_path_subdirectories(path: Path):
    return [i for i in path.iterdir() if i.is_dir]


def chain_flatten(lst: Iterable[Iterable[T]]) -> list[T]:
    return list(chain.from_iterable(lst))


def set_difference(s_large: Iterable, s2: Iterable):
    return list(set(s_large).difference(set(s2)))
