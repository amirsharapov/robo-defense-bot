from dataclasses import dataclass
from functools import cache, cached_property
from typing import Literal

from src.game.constants import TOWER_MENU_BR_XY, TOWER_MENU_TR_XY, TOWER_MENU_BL_XY, TOWER_MENU_TL_XY
from src.libs.geometry import Point


@dataclass
class TowerCategory:
    id: str
    name: str

    def __hash__(self):
        return hash(self.id)


@dataclass
class Tower:
    id: str

    @cached_property
    def category(self) -> TowerCategory | None:
        return get_tower_category(self.id)

    @cached_property
    def category_id(self) -> str:
        return self.id[:2]

    @cached_property
    def level(self) -> int:
        return int(self.id[2:3])

    @cached_property
    def upgrade_path(self) -> list['Tower']:
        return get_tower_upgrade_path(self.id)

    @cached_property
    def upgrade_options(self) -> list['UpgradeOption']:
        return get_tower_upgrade_options(self.id)

    @cached_property
    def upgrade_options_map(self) -> dict[str, 'UpgradeOption']:
        return get_tower_upgrade_options_map(self.id)

    def __hash__(self):
        return hash(self.id)

    def get_upgrade_option(self, target_tower_id: str) -> 'UpgradeOption | None':
        return get_tower_upgrade_option(self.id, target_tower_id)


@dataclass
class UpgradeOption:
    source_tower_id: str
    target_tower_id: str
    position: str | Literal['tr', 'br', 'bl', 'tl']

    @property
    def position_xy(self) -> Point:
        return {
            'tr': TOWER_MENU_TR_XY,
            'br': TOWER_MENU_BR_XY,
            'bl': TOWER_MENU_BL_XY,
            'tl': TOWER_MENU_TL_XY
        }[self.position]


_tower_categories = [
    # base towers
    TowerCategory('gu', 'gun'),
    TowerCategory('ro', 'rocket'),
    TowerCategory('sl', 'slow'),
    # gun upgrades
    TowerCategory('fm', 'flame'),
    TowerCategory('aa', 'anti_air_cannon'),
    # rocket upgrades
    TowerCategory('mo', 'mortar'),
    TowerCategory('sa', 'surface_to_air_missile'),
    # slow upgrades
    TowerCategory('te', 'teleport'),
    TowerCategory('mi', 'mine'),
    # mine upgrades
    TowerCategory('fr', 'flare')
]

_towers = [
    # base towers
    # gun towers lvl 1 - 3
    Tower('gu1'),
    Tower('gu2'),
    Tower('gu3'),
    # rocket towers lvl 1 - 3
    Tower('ro1'),
    Tower('ro2'),
    Tower('ro3'),
    # slow towers lvl 1 - 3
    Tower('sl1'),
    Tower('sl2'),
    Tower('sl3'),

    # gun specializations lvl 1 - 2
    # flame tower lvl 1 - 2
    Tower('fm1'),
    Tower('fm2'),
    # anti-air cannon lvl 1 - 2
    Tower('aa1'),
    Tower('aa2'),

    # rocket specializations lvl 1 - 2
    # mortar lvl 1 - 2
    Tower('mo1'),
    Tower('mo2'),
    # surface-to-air missile lvl 1 - 2
    Tower('sa1'),
    Tower('sa2'),

    # slow specializations lvl 1 - 2
    # teleport tower lvl 0 - 1
    Tower('te0'),
    Tower('te1'),
    # mine tower lvl 0 - 1
    Tower('mi0'),
    Tower('mi1'),
    # flare tower lvl 1
    Tower('fr1')
]

_tower_upgrades = {
    # gun towers
    'gu1': ['gu2', 'fm1', 'aa1'],
    'gu2': ['gu3'],
    'fm1': ['fm2'],
    'aa1': ['aa2'],
    # rocket towers
    'ro1': ['ro2', 'mo1', 'sa1'],
    'ro2': ['ro3'],
    'mo1': ['mo2'],
    'sa1': ['sa2'],
    # slow towers
    'sl1': ['sl2', 'te0', 'mi0'],
    'sl2': ['sl3'],
    'te0': ['te1'],
    'mi0': ['mi1', 'fr1']
}


@cache
def get_tower_categories_map():
    return {tc.id: tc for tc in _tower_categories}


@cache
def get_towers_map():
    return {t.id: t for t in _towers}


@cache
def get_tower_upgrades_map():
    return _tower_upgrades


@cache
def get_reversed_tower_upgrades_map():
    result = {}
    for tower, upgrades in _tower_upgrades.items():
        if tower not in result:
            result[tower] = None
        for upgrade in upgrades:
            result[upgrade] = tower
    return result


def get_tower(tower_id: str) -> Tower | None:
    return get_towers_map().get(tower_id)


def get_tower_category(category_id: str) -> TowerCategory | None:
    return get_tower_categories_map().get(category_id)


@cache
def get_tower_upgrade_path(tower_id: str):
    result = []
    current_tower_id = tower_id
    while current_tower_id is not None:
        result.append(current_tower_id)
        current_tower_id = get_reversed_tower_upgrades_map().get(current_tower_id)
    result.reverse()
    result = [get_tower(tid) for tid in result if get_tower(tid) is not None]
    return result


@cache
def get_tower_upgrade_options(tower_id: str) -> list[UpgradeOption]:
    positions = ['tr', 'br', 'bl', 'tl']
    # skip "tl" position because that is sell button
    positions = positions[:-1]

    target_tower_ids = get_tower_upgrades_map().get(tower_id, [])
    assert len(target_tower_ids) <= len(positions)

    result = []
    for position, target_tower_id in zip(positions, target_tower_ids):
        result.append(
            UpgradeOption(
                source_tower_id=tower_id,
                target_tower_id=target_tower_id,
                position=position
            )
        )

    return result


@cache
def get_tower_upgrade_options_map(tower_id: str) -> dict[str, UpgradeOption]:
    upgrade_options = get_tower_upgrade_options(tower_id)
    return {uo.target_tower_id: uo for uo in upgrade_options}


@cache
def get_tower_upgrade_option(tower_id: str, target_tower_id: str) -> UpgradeOption | None:
    upgrade_options_map = get_tower_upgrade_options_map(tower_id)
    return upgrade_options_map.get(target_tower_id)
