from pathlib import Path

import cv2

from src.libs.android import screenshot


def get_next_filename():
    files = list(Path('local/screenshots').iterdir())
    files = [f.name.removeprefix('screenshot').removesuffix('.png') for f in files]
    files = [int(f) for f in files if f.isdigit()]
    next_i = max(files, default=0) + 1
    return Path('local/screenshots') / f'screenshot{next_i}.png'


def screenshot_for_test():
    data = screenshot()
    file = get_next_filename().as_posix()
    cv2.imwrite(file, data)


if __name__ == "__main__":
    screenshot_for_test()
