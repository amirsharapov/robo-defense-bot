from enum import auto

from src.libs.enums import BaseEnum


class Towers(BaseEnum):
    GUN = auto()
    ROCKET = auto()
    SLOW = auto()


class Upgrades(BaseEnum):
    GUN_2 = auto()
    GUN_3 = auto()
    ROCKET_2 = auto()
    ROCKET_3 = auto()
    SLOW_2 = auto()
    SLOW_3 = auto()
    ANTI_AIR_MISSILE = auto()
    ANTI_AIR_MISSILE_2 = auto()
