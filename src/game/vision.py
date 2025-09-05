import cv2
from numpy import ndarray

from src.libs.android import screenshot
from src.libs.utils import first_or_none
from src.libs.vision import match_template
from src.paths import get_templates_path


def locate_template(
        name: str,
        image: ndarray | None = None,
        threshold: float = 0.8,
        use_mask: bool = False
):
    if image is None:
        image = screenshot()

    template = str(get_templates_path() / name)
    template = cv2.imread(template)

    return match_template(
        image=image,
        template=template,
        threshold=threshold,
        use_mask=use_mask
    )


def locate_first_template(
        name: str,
        image: ndarray | None = None,
        threshold: float = 0.8,
        use_mask: bool = False
):
    matches = locate_template(
        name=name,
        image=image,
        threshold=threshold,
        use_mask=use_mask
    )
    return first_or_none(matches)


def locate_game_icon(image: ndarray | None = None):
    return locate_first_template(
        name='game_icon.png',
        image=image,
        threshold=0.8,
    )


def locate_exit_anchor(image: ndarray | None = None):
    return locate_first_template(
        name='basic_level/anchor.png',
        image=image,
        threshold=0.8,
    )


def locate_start_game_button(image: ndarray | None = None):
    return locate_first_template(
        name='basic_level/start_game_button.png',
        image=image,
        threshold=0.8,
    )


def locate_you_win_message(image: ndarray | None = None):
    return locate_first_template(
        name='you_win_message.png',
        image=image,
        threshold=0.6,
        use_mask=True
    )


def locate_new_game_button(image: ndarray | None = None):
    return locate_first_template(
        name='main_menu/new_game_button.png',
        image=image,
        threshold=0.8,
    )
