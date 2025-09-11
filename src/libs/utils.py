from pathlib import Path
from typing import Iterable, TypeVar

_T = TypeVar('_T')


def first_or_none(iterable: Iterable[_T]) -> _T | None:
    return next(iter(iterable), None)


def get_next_local_screenshot_filename():
    files = list(Path('local/screenshots').iterdir())
    files = [f.name.removeprefix('screenshot').removesuffix('.png') for f in files]
    files = [int(f) for f in files if f.isdigit()]
    next_i = max(files, default=0) + 1
    return Path('local/screenshots') / f'screenshot{next_i}.png'
