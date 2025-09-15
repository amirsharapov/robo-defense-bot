import time
from enum import auto
from typing import Literal

import cv2
import numpy as np
import requests

from src import env, templates
from src.libs import adb, event_logger
from src.libs.adb import WakefulnessStates, send_power_keyevent, swipe, MotionEvents
from src.libs.enums import BaseEnum
from src.libs.geometry import Point, Line
from src.libs.io import TemporaryFile
from src.libs.subprocess import ExecuteCommnadResponse
from src.libs.utils import first_or_none
from src.libs.vision import match_template


class ScreenshotStrategies(BaseEnum):
    ADB = auto()
    API = auto()


def screenshot(strategy: ScreenshotStrategies | Literal['abd', 'api'] = 'api', quality: int = 100):
    if isinstance(strategy, str):
        strategy = ScreenshotStrategies(strategy)

    if strategy == ScreenshotStrategies.ADB:
        return screenshot_with_adb()

    if strategy == ScreenshotStrategies.API:
        return screenshot_with_api(quality)

    raise ValueError(f'Unknown screenshot strategy: {strategy}')


def screenshot_with_adb():
    with TemporaryFile.random_filename() as file:
        adb.screencap(file.path)
        image = cv2.imread(str(file.path))
        event_logger.log_screenshot_event(image)
        return image


def screenshot_with_api(quality: int = 100):
    url = env.SCREENSHOT_API_URL.get()

    response = requests.get(url, params={'quality': quality})
    response.raise_for_status()

    image = cv2.imdecode(
        np.frombuffer(response.content, np.uint8),
        cv2.IMREAD_COLOR
    )

    return image


def accept_tablet_data_permissions():
    image = screenshot()

    template = templates.get_template_by_name('android/prompts/allow_access_to_tablet_data/prompt.png')
    match = first_or_none(
        match_template(
            image=image,
            template=template.read_image(),
            threshold=template.threshold
        )
    )

    if not match:
        return

    template = templates.get_template_by_name('android/prompts/allow_access_to_tablet_data/allow_button.png')
    match = first_or_none(
        match_template(
            image=image,
            template=template.read_image(),
            threshold=template.threshold,
            region=match.rectangle
        )
    )

    if not match:
        return

    x, y = match.rect.center
    adb.tap(x, y)


def go_to_home_screen():
    adb.send_home_keyevent()
    time.sleep(1)


def go_back():
    adb.send_back_keyevent()
    time.sleep(1)


def unlock() -> bool:
    dreaming_lockscreen = adb.get_dreaming_lockscreen()
    state = adb.get_wakefulness_state()

    if state == WakefulnessStates.AWAKE and not dreaming_lockscreen:
        print("Device is already awake and unlocked.")
        return False

    if state == WakefulnessStates.DOZING or state == WakefulnessStates.ASLEEP:
        print("Device is dozing, waking it up.")
        send_power_keyevent()
        time.sleep(1)

    if state == WakefulnessStates.DREAMING:
        print("Device is dreaming, waking it up.")
        swipe(400, 400, 800, 400)
        time.sleep(1)

    # we can't tell if we opened the passcode screen or not, so we just assume no
    swipe(400, 400, 800, 400)
    time.sleep(1)

    passcode = env.DEVICE_PASSCODE.get()
    adb.send_text(passcode)
    adb.send_enter_keyevent()
    time.sleep(1)

    return True


def setup_screenshot_api_port_forwarding():
    local_port = env.SCREENSHOT_API_URL.get().split(':')[-1]
    device_port = 8080
    e: Exception | None = None
    result: ExecuteCommnadResponse | None = None

    for i in range(2):
        try:
            result = adb.forward(local_port, device_port)
        except Exception as _e:
            e = _e
            print(f"Attempt {i + 1} failed: {e}")
            time.sleep(1)

    if not result:
        raise e


def tap_middle_of_screen():
    tap_point(
        Point(
            MAX_X // 2,
            MAX_Y // 2
        )
    )


def tap_point(point: Point):
    adb.tap(point.x, point.y)


def swipe_using_motion_events(x1: int, y1: int, x2: int, y2: int, steps: int = 10, delay_between_steps: float = 0.01):
    line = Line(
        point1=Point(x1, y1),
        point2=Point(x2, y2)
    )

    adb.send_motion_event(
        MotionEvents.DOWN,
        line.point1.x,
        line.point1.y
    )

    time.sleep(0.1)

    points = line.linspace(steps=steps)
    for point in points:
        adb.send_motion_event(
            MotionEvents.MOVE,
            int(point.x),
            int(point.y)
        )
        time.sleep(delay_between_steps)

    time.sleep(0.1)
    adb.send_motion_event(
        MotionEvents.UP,
        line.point2.x,
        line.point2.y
    )

    time.sleep(1)


def swipe_towards_direction(direction: str | Literal['up', 'down', 'left', 'right']):
    center_x = MAX_X // 2
    center_y = MAX_Y // 2
    offset = 250

    if direction == 'up':
        start = Point(center_x, center_y + offset)
        end = Point(center_x, center_y - offset)
    elif direction == 'down':
        start = Point(center_x, center_y - offset)
        end = Point(center_x, center_y + offset)
    elif direction == 'left':
        start = Point(center_x + offset, center_y)
        end = Point(center_x - offset, center_y)
    elif direction == 'right':
        start = Point(center_x - offset, center_y)
        end = Point(center_x + offset, center_y)
    else:
        raise ValueError(f'Unknown direction: {direction}')

    swipe_using_motion_events(
        start.x,
        start.y,
        end.x,
        end.y
    )

    time.sleep(0.25)


MAX_X = 1340
MAX_Y = 800
