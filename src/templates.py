from dataclasses import dataclass
from functools import cache, cached_property

import cv2

from src.paths import get_templates_path


# should match the templates directory structure


@dataclass
class Template:
    name: str
    threshold: float
    use_mask: bool = False

    @cached_property
    def path(self):
        return get_templates_path() / self.name

    def read_image(self):
        path = str(self.path)
        return cv2.imread(path, cv2.IMREAD_UNCHANGED)


_templates = [
    Template(
        name='android/prompts/allow_access_to_tablet_data/prompt.png',
        threshold=0.8,
    ),
    Template(
        name='android/prompts/allow_access_to_tablet_data/allow_button.png',
        threshold=0.8,
    ),
    Template(
        name='android/robo_defense_icon.png',
        threshold=0.8,
    ),
    Template(
        name='game/basic_level/anchor.png',
        threshold=0.8,
    ),
    Template(
        name='game/basic_level/start_game_button.png',
        threshold=0.8,
    ),
    Template(
        name='game/main_menu/prompts/discard_game_and_start_over/prompt_v1.png',
        threshold=0.8,
    ),
    Template(
        name='game/main_menu/prompts/discard_game_and_start_over/prompt_v2.png',
        threshold=0.8,
    ),
    Template(
        name='game/main_menu/prompts/discard_game_and_start_over/yes_button_v1.png',
        threshold=0.8,
    ),
    Template(
        name='game/main_menu/prompts/discard_game_and_start_over/yes_button_v2.png',
        threshold=0.8,
    ),
    Template(
        name='game/main_menu/new_game_button.png',
        threshold=0.8,
    ),
    Template(
        name='game/main_menu/reward_points_button.png',
        threshold=0.8,
    ),
    Template(
        name='game/tower_upgrades/aa1.png',
        threshold=0.6,
        use_mask=True
    ),
    Template(
        name='game/tower_upgrades/aa2.png',
        threshold=0.6,
        use_mask=True
    ),
    Template(
        name='game/tower_upgrades/gu2.png',
        threshold=0.6,
        use_mask=True
    ),
    Template(
        name='game/tower_upgrades/gu3.png',
        threshold=0.6,
        use_mask=True
    ),
    Template(
        name='game/tower_upgrades/sa1.png',
        threshold=0.6,
        use_mask=True
    ),
    Template(
        name='game/tower_upgrades/sa2.png',
        threshold=0.6,
        use_mask=True
    ),
    Template(
        name='game/tower_upgrades/sl2.png',
        threshold=0.6,
        use_mask=True
    ),
    Template(
        name='game/tower_upgrades/sl3.png',
        threshold=0.6,
        use_mask=True
    ),
    Template(
        name='game/you_win_message.png',
        threshold=0.6,
        use_mask=True
    )
]


@cache
def get_templates_by_name_map() -> dict:
    return {t.name: t for t in _templates}


@cache
def get_template_by_name(name: str) -> Template:
    assert name in get_templates_by_name_map(), f'Template not found: {name}'
    return get_templates_by_name_map().get(name)
