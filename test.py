import cv2

from src.game.planner import read_plan


def test():
    read_plan('data/src/plans/basic_level_v1/1')


if __name__ == "__main__":
    test()
