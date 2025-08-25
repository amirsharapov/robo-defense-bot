import time

import cv2

from src.game.client import toggle_pause_button, place_tower, toggle_fast_forward_button, place_towers, upgrade_towers, \
    place_and_upgrade_towers
from src.game.enums import Towers, Upgrades
from src.game.grid import AnchorTypes, generate_grid
from src.game.vision import locate_gun_towers
from src.libs.android import screenshot
from src.libs.vision import match_template


def main():
    # toggle_pause_button()

    # first line of towers to block the path

    place_towers([
        (6, 0, 'gun'),
        (6, 1, 'gun'),
        (6, 2, 'gun'),
        (5, 2, 'gun'),
        (4, 2, 'slow'),
        (3, 2, 'gun'),
        (2, 2, 'gun'),
        (0, 2, 'gun')
    ])

    toggle_fast_forward_button()

    # next line of towers to keep path blocked

    place_towers([
        (0, 3, 'gun'),
        (0, 4, 'gun'),
        (1, 4, 'gun'),
        (2, 4, 'slow'),
        (3, 4, 'gun'),
        (4, 4, 'gun'),
        (5, 4, 'gun'),
        (6, 4, 'slow'),
        (7, 4, 'gun'),
        (9, 4, 'gun')
    ])

    # next line is to improve firepower and more guns

    place_and_upgrade_towers([
        (4, 0, 'gun', ['gun_2', 'gun_3']),
        (3, 0, 'gun', ['gun_2', 'gun_3']),
        (2, 0, 'slow', []),
        (1, 0, 'gun', ['gun_2', 'gun_3']),
        (0, 0, 'gun', ['gun_2', 'gun_3']),
        (0, 1, 'gun', ['gun_2', 'gun_3'])
    ])

    # upgrade all the towers already placed so far

    upgrade_towers([
        (6, 0, ['gun_2', 'gun_3']),
        (6, 1, ['gun_2', 'gun_3']),
        (6, 2, ['gun_2', 'gun_3']),
        (5, 2, ['gun_2', 'gun_3']),
        (4, 2, []),
        (3, 2, ['gun_2', 'gun_3']),
        (2, 2, ['gun_2', 'gun_3']),
        (0, 2, ['gun_2', 'gun_3']),
        (0, 3, ['gun_2', 'gun_3']),
        (0, 4, ['gun_2', 'gun_3']),
        (1, 4, ['gun_2', 'gun_3']),
        (2, 4, []),
        (3, 4, ['gun_2', 'gun_3']),
        (4, 4, ['gun_2', 'gun_3']),
        (5, 4, ['gun_2', 'gun_3']),
        (6, 4, []),
        (7, 4, ['gun_2', 'gun_3']),
        (9, 4, ['gun_2', 'gun_3'])
    ])

    # temporary for air defense

    place_and_upgrade_towers([
        (5, 5, 'gun', ['gun_2', 'gun_3']),
        (5, 6, 'gun', ['gun_2', 'gun_3']),
        (5, 7, 'gun', ['gun_2', 'gun_3']),
        (5, 8, 'gun', ['gun_2', 'gun_3']),
        (5, 9, 'gun', ['gun_2', 'gun_3']),
        (5, 10, 'gun', ['gun_2', 'gun_3']),
        (5, 11, 'gun', ['gun_2', 'gun_3']),
        (5, 12, 'gun', ['gun_2', 'gun_3']),
        (5, 13, 'gun', ['gun_2', 'gun_3']),
        (5, 14, 'gun', ['gun_2', 'gun_3']),
        (5, 15, 'gun', ['gun_2', 'gun_3']),
        (5, 16, 'gun', ['gun_2', 'gun_3']),
        (4, 6, 'slow', []),
        (6, 8, 'slow', [])
    ])



if __name__ == "__main__":
    main()
