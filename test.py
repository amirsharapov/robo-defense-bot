import cv2

from src.game.utils import get_template_matches


def test():
    image = cv2.imread('local/screenshots/screenshot18.png')
    matches = get_template_matches(
        template_name='game/tower_upgrades/gu3.png',
        image=image
    )

    assert len(matches) == 1, f'Expected 1 match, got {len(matches)}'


if __name__ == "__main__":
    test()
