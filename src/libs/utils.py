from typing import Iterable, TypeVar

_T = TypeVar('_T')


def first_or_none(iterable: Iterable[_T]) -> _T | None:
    return next(iter(iterable), None)
