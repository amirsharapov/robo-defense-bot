import cv2

from src.game.planner import read_plan
from src.game.utils import get_first_template_match


def test():
    image = cv2.imread('local/screenshots/screenshot32.png')
    match = get_first_template_match('game/tower_purchases/ro.png', image)
    print('ro', match)
    match = get_first_template_match('game/tower_purchases/gu.png', image)
    print('gu', match)
    match = get_first_template_match('game/tower_purchases/sl.png', image)
    print('sl', match)
    image = cv2.imread('local/screenshots/screenshot34.png')
    match = get_first_template_match('game/tower_purchases/ro.png', image)
    print('ro', match)
    match = get_first_template_match('game/tower_purchases/gu.png', image)
    print('gu', match)
    match = get_first_template_match('game/tower_purchases/sl.png', image)
    print('sl', match)


if __name__ == "__main__":
    test()
