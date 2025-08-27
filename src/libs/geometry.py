from dataclasses import dataclass

import numpy as np


@dataclass
class Rectangle:
    x: int
    y: int
    w: int
    h: int

    @property
    def center(self):
        return Point(
            self.x + self.w // 2,
            self.y + self.h // 2
        )

    @property
    def x1(self) -> int:
        return self.x

    @property
    def y1(self) -> int:
        return self.y

    @property
    def x2(self) -> int:
        return self.x + self.w

    @property
    def y2(self) -> int:
        return self.y + self.h

    def __post_init__(self):
        self.w = int(self.w)
        self.h = int(self.h)
        self.x = int(self.x)
        self.y = int(self.y)

    def to_xyxy(self):
        return self.x1, self.y1, self.x2, self.y2


@dataclass
class Point:
    x: int
    y: int

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, index):
        return tuple(self)[index]

    def __hash__(self):
        return hash((self.x, self.y))

    def translated(self, dx: int = 0, dy: int = 0) -> 'Point':
        return Point(self.x + dx, self.y + dy)


@dataclass
class Line:
    point1: Point
    point2: Point

    @property
    def x1(self):
        return self.point1.x

    @property
    def y1(self):
        return self.point1.y

    @property
    def x2(self):
        return self.point2.x

    @property
    def y2(self):
        return self.point2.y

    def linspace(self, steps: int):
        xs = np.linspace(self.x1, self.x2, steps, dtype=int)
        ys = np.linspace(self.y1, self.y2, steps, dtype=int)
        return [Point(x, y) for x, y in zip(xs, ys)]