import cv2
from numpy import ndarray

from src.libs.android import screenshot
from src.libs.utils import first_or_none
from src.libs.vision import match_template
from src.paths import get_templates_path


def locate_exit_anchor(image: ndarray | None = None):
    if image is None:
        image = screenshot()

    template = str(get_templates_path() / 'basic_level/anchor.png')
    template = cv2.imread(template)

    return first_or_none(
        match_template(
            image=image,
            template=template,
            threshold=0.8
        )
    )


def locate_start_game_button(image: ndarray | None = None):
    if image is None:
        image = screenshot()

    template = str(get_templates_path() / 'basic_level/start_game_button.png')
    template = cv2.imread(template)

    return first_or_none(
        match_template(
            image=image,
            template=template,
            threshold=0.8
        )
    )


def locate_gun_towers(image: ndarray | None = None):
    if image is None:
        image = screenshot()

    template = str(get_templates_path() / 'towers/gun_tower.png')
    template = cv2.imread(template)

    return match_template(
        image=image,
        template=template
    )


def locate_rocket_towers(image: ndarray | None = None):
    if image is None:
        image = screenshot()

    template = str(get_templates_path() / 'towers/rocket_tower.png')
    template = cv2.imread(template)

    return match_template(
        image=image,
        template=template
    )


def locate_slow_towers(image: ndarray | None = None):
    if image is None:
        image = screenshot()

    template = str(get_templates_path() / 'towers/slow_tower.png')
    template = cv2.imread(template)

    return match_template(
        image=image,
        template=template
    )
