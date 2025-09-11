import cv2

from src.libs.android import screenshot
from src.libs.utils import get_next_local_screenshot_filename


def screenshot_for_test():
    data = screenshot()
    file = get_next_local_screenshot_filename().as_posix()
    cv2.imwrite(file, data)


if __name__ == "__main__":
    screenshot_for_test()
