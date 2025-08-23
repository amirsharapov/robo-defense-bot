from enum import auto
from pathlib import Path

from src.libs.enums import BaseEnum
from src.libs.subprocess import execute_command

MAX_X = 1340
MAX_Y = 800
ADB_EXE = "~/Code/bin/platform-tools/adb"


class ADBInputSources(BaseEnum):
    TAP = auto()
    SWIPE = auto()
    TEXT = auto()
    KEYEVENT = auto()


class WakefulnessStates(BaseEnum):
    ASLEEP = auto()
    AWAKE = auto()
    DOZING = auto()
    DREAMING = auto()
    UNKNOWN = auto()

    @classmethod
    def _missing_(cls, value):
        raise ValueError(f"Unknown wakefulness state: {value}.")


def make_shell_input_tap_command(x: int, y: int) -> str:
    cmd = f'{ADB_EXE} shell input tap {x} {y}'
    return cmd


def make_shell_input_swipe_command(x1: int, y1: int, x2: int, y2: int) -> str:
    cmd = f'{ADB_EXE} shell input swipe {x1} {y1} {x2} {y2}'
    return cmd


def make_shell_input_text_command(text: str) -> str:
    cmd = f'{ADB_EXE} shell input text "{text}"'
    return cmd


def make_shell_input_keyevent_command(keyevent: str) -> str:
    cmd = f'{ADB_EXE} shell input keyevent {keyevent}'
    return cmd


def make_dumpsys_command_with_grep(service: str, grep: str) -> str:
    cmd = f'{ADB_EXE} shell dumpsys {service} | grep -E "{grep}"'
    return cmd


def make_screencap_command(path: str | Path) -> str:
    path = Path(path)
    return f'{ADB_EXE} exec-out screencap -p > "{path.absolute().as_posix()}"'


def get_wakefulness_state():
    cmd = make_dumpsys_command_with_grep("power", "mWakefulness=")
    output = execute_command(cmd)
    state = output.split('=')[-1].strip().upper()
    return WakefulnessStates(state)


def send_keyevent(keyevent: str):
    cmd = make_shell_input_keyevent_command(keyevent)
    execute_command(cmd)


def send_power_keyevent():
    send_keyevent('26')


def send_enter_keyevent():
    send_keyevent('66')


def swipe(x1: int, y1: int, x2: int, y2: int):
    cmd = make_shell_input_swipe_command(x1, y1, x2, y2)
    execute_command(cmd)


def get_dreaming_lockscreen():
    cmd = make_dumpsys_command_with_grep("window", "mDreamingLockscreen=")
    output = execute_command(cmd)
    state = output.split('=')[-1].strip().upper()
    return state == "TRUE"


def send_text(text: str):
    cmd = make_shell_input_text_command(text)
    execute_command(cmd)


def screencap(path: str | Path):
    cmd = make_screencap_command(path)
    execute_command(cmd)
