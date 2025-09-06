import cv2

from src.libs.android import screenshot


def screenshot_for_test():
    data = screenshot()
    cv2.imwrite('screenshot11.png', data)


if __name__ == "__main__":
    screenshot_for_test()
