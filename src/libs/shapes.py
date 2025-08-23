from dataclasses import dataclass


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