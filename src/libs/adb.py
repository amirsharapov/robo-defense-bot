from enum import auto
from pathlib import Path

from src.libs.enums import BaseEnum
from src.libs.subprocess import execute_command

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


class MotionEvents(BaseEnum):
    DOWN = auto()
    UP = auto()
    MOVE = auto()
    CANCEL = auto()


def make_shell_input_tap_command(x: int, y: int) -> str:
    cmd = f'{ADB_EXE} shell input tap {x} {y}'
    return cmd


def make_shell_input_swipe_command(x1: int, y1: int, x2: int, y2: int, duration_ms: int = None) -> str:
    cmd = f'{ADB_EXE} shell input swipe {x1} {y1} {x2} {y2}'
    if duration_ms is not None:
        cmd += f' {duration_ms}'
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


def make_motion_event_command(motion_event: MotionEvents, x: int, y: int) -> str:
    cmd = f'{ADB_EXE} shell input motionevent {motion_event.name.lower()} {x} {y}'
    return cmd


def make_screencap_command(path: str | Path) -> str:
    path = Path(path)
    return f'{ADB_EXE} exec-out screencap -p > "{path.absolute().as_posix()}"'


def make_forward_command(local_port: int, device_port: int) -> str:
    cmd = f'{ADB_EXE} forward tcp:{local_port} tcp:{device_port}'
    return cmd


def get_wakefulness_state():
    cmd = make_dumpsys_command_with_grep("power", "mWakefulness=")
    result = execute_command(cmd)

    output = None
    for line in result.stdout.splitlines():
        if 'mWakefulness=' in line:
            output = line.strip()
            break

    if output is None:
        raise RuntimeError("Could not find 'mWakefulness' in dumpsys output.")

    state = output.split('=')[-1].strip().upper()
    return WakefulnessStates(state)


def send_keyevent(keyevent: str):
    cmd = make_shell_input_keyevent_command(keyevent)
    return execute_command(cmd)


def send_power_keyevent():
    return send_keyevent('26')


def send_enter_keyevent():
    return send_keyevent('66')


def swipe(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 500):
    cmd = make_shell_input_swipe_command(x1, y1, x2, y2, duration_ms)
    return execute_command(cmd)


def tap(x: int, y: int):
    cmd = make_shell_input_tap_command(x, y)
    return execute_command(cmd)


def send_motion_event(motion_event: MotionEvents, x: int, y: int):
    cmd = make_motion_event_command(motion_event, x, y)
    return execute_command(cmd)


def get_dreaming_lockscreen():
    cmd = make_dumpsys_command_with_grep("window", "mDreamingLockscreen=")
    result = execute_command(cmd)

    output = None
    for line in result.stdout.splitlines():
        if 'mDreamingLockscreen=' in line:
            output = line.strip()
            break

    if output is None:
        raise RuntimeError("Could not find 'mDreamingLockscreen' in dumpsys output.")

    state = output.split('=')[-1].strip().upper()
    return state == "TRUE"


def send_text(text: str):
    cmd = make_shell_input_text_command(text)
    return execute_command(cmd)


def screencap(path: str | Path):
    cmd = make_screencap_command(path)
    return execute_command(cmd)


def forward(local_port: int, device_port: int):
    cmd = make_forward_command(local_port, device_port)
    return execute_command(cmd)


def send_home_keyevent():
    return send_keyevent('KEYCODE_HOME')


def send_back_keyevent():
    return send_keyevent('KEYCODE_BACK')


def send_monkey_event(package_name: str, category_name: str, count: int = 1):
    cmd = f'{ADB_EXE} shell monkey -p {package_name} -c {category_name} {count}'
    return execute_command(cmd, raise_error=False)
