import time
from enum import auto
from typing import Literal

import cv2
import numpy as np
import requests

from src import env
from src.libs import adb, event_logger
from src.libs.adb import WakefulnessStates, send_power_keyevent, swipe
from src.libs.enums import BaseEnum
from src.libs.io import TemporaryFile


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


def unlock():
    dreaming_lockscreen = adb.get_dreaming_lockscreen()
    state = adb.get_wakefulness_state()

    if state == WakefulnessStates.AWAKE and not dreaming_lockscreen:
        print("Device is already awake and unlocked.")
        return

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


def setup_screenshot_api_port_forwarding():
    local_port = env.SCREENSHOT_API_URL.get().split(':')[-1]
    device_port = 8080
    result = adb.forward(local_port, device_port)
    print(result.stdout)


def tap(x: int, y: int, *, debug_context: dict = None):
    ...