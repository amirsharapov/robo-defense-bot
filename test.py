import cv2

from src.game.planner import read_plan
from src.game.utils import get_first_template_match, get_template_matches


def test():
    # image = cv2.imread('local/screenshots/screenshot32.png')
    # match = get_first_template_match('game/tower_purchases/ro.png', image)
    # print('ro', match)
    # match = get_first_template_match('game/tower_purchases/gu.png', image)
    # print('gu', match)
    # match = get_first_template_match('game/tower_purchases/sl.png', image)
    # print('sl', match)
    # image = cv2.imread('local/screenshots/screenshot34.png')
    # match = get_first_template_match('game/tower_purchases/ro.png', image)
    # print('ro', match)
    # match = get_first_template_match('game/tower_purchases/gu.png', image)
    # print('gu', match)
    # match = get_first_template_match('game/tower_purchases/sl.png', image)
    # print('sl', match)
    image = cv2.imread('local/screenshots/screenshot36.png')
    matches = get_template_matches('game/main_menu/down_button.png', image)
    print('down_button', matches)


if __name__ == "__main__":
    test()
