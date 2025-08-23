from enum import auto

from src.libs.enums import BaseEnum


class TowerTypes(BaseEnum):
    GUN = auto()
    ROCKET = auto()
    SLOW = auto()
