# unique ID for the execution of the program
import time
import uuid
from enum import auto
from pathlib import Path

import cv2
import numpy as np

from src.paths import get_logs_dir

_logger_id: str | None = None
_logger_level: str = 'info'


def get_logger_id() -> str:
    global _logger_id
    if _logger_id is None:
        _logger_id = str(uuid.uuid4())
    return _logger_id


def get_session_dir() -> Path:
    root = get_logs_dir() / get_logger_id()
    root.mkdir(parents=True, exist_ok=True)
    return root


def log_screenshot_event(image: np.ndarray):
    if _logger_level == 'debug':
        path = get_session_dir() / str(time.time()).replace('.', '_')
        path = path.with_suffix('.png')
        cv2.imwrite(str(path), image)


def log_tap_event(x, y):
    pass


def log_swipe_event(x1, y1, x2, y2, duration_ms):
    pass


def log_grid_generated_event(grid):
    pass
