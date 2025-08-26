from dataclasses import dataclass


@dataclass
class TowerCategory:
    shortcode: str
    name: str


@dataclass
class Tower:
    category_shortcode: str
    level: int

    @property
    def shortcode(self) -> str:
        return f"{self.category_shortcode}{self.level}"


tower_categories = [
    # base towers
    TowerCategory('GU', 'gun'),
    TowerCategory('RO', 'rocket'),
    TowerCategory('SL', 'slow'),
    # gun upgrades
    TowerCategory('FM', 'flame'),
    TowerCategory('AA', 'anti_air_cannon'),
    # rocket upgrades
    TowerCategory('MO', 'mortar'),
    TowerCategory('SA', 'surface_to_air_missile'),
    # slow upgrades
    TowerCategory('TE', 'teleport'),
    TowerCategory('MI', 'mine'),
    # mine upgrades
    TowerCategory('FR', 'flare')
]

tower_types_by_shortcode = {tt.shortcode: tt for tt in tower_categories}

towers = [
    # base towers
    # gun towers lvl 1 - 3
    Tower('GU', 1),
    Tower('GU', 2),
    Tower('GU', 3),
    # rocket towers lvl 1 - 3
    Tower('RO', 1),
    Tower('RO', 2),
    Tower('RO', 3),
    # slow towers lvl 1 - 3
    Tower('SL', 1),
    Tower('SL', 2),
    Tower('SL', 3),

    # gun specializations lvl 1 - 2
    # flame tower lvl 1 - 2
    Tower('FM', 1),
    Tower('FM', 2),
    # anti-air cannon lvl 1 - 2
    Tower('AA', 1),
    Tower('AA', 2),

    # rocket specializations lvl 1 - 2
    # mortar lvl 1 - 2
    Tower('MO', 1),
    Tower('MO', 2),
    # surface-to-air missile lvl 1 - 2
    Tower('SA', 1),
    Tower('SA', 2),

    # slow specializations lvl 1 - 2
    # teleport tower lvl 0 - 1
    Tower('TE', 0),
    Tower('TE', 1),
    # mine tower lvl 0 - 1
    Tower('MI', 0),
    Tower('MI', 1),
    # flare tower lvl 1
    Tower('FR', 1)
]

tower_upgrades = {
    'GU1': ['GU2', 'FM1', 'AA1'],
    'GU2': ['GU3'],
    'FM1': ['FM2'],
    'AA1': ['AA2'],
    'RO1': ['RO2', 'MO1', 'SA1'],
    'RO2': ['RO3'],
    'MO1': ['MO2'],
    'SA1': ['SA2'],
    'SL1': ['SL2', 'TE0', 'MI0'],
    'SL2': ['SL3'],
    'TE0': ['TE1'],
    'MI0': ['MI1', 'FR1'],
}
