import time

import cv2

from src import env
from src.libs import adb
from src.libs.adb import WakefulnessStates, send_power_keyevent, swipe
from src.libs.io import TemporaryFile


def screenshot():
    with TemporaryFile.random_filename() as file:
        adb.screencap(file.path)
        return cv2.imread(str(file.path))


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
