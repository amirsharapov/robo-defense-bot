import time
from collections.abc import Callable

from numpy import ndarray

from src import templates
from src.libs import android, vision, adb
from src.libs.utils import first_or_none


def _default_check_interval_fn(iteration: int):
    if iteration < 25:
        return 0.5
    return 1


def get_template_matches(template_name: str, image: ndarray | None = None):
    template = templates.get_template_by_name(template_name)

    if image is None:
        image = android.screenshot()

    return vision.match_template(
        image=image,
        template=template.read_image(),
        threshold=template.threshold,
        use_mask=template.use_mask
    )


def get_first_template_match(template_name: str, image: ndarray | None = None):
    return first_or_none(
        get_template_matches(
            template_name,
            image
        )
    )


def tap_first_template_match(template_name: str):
    match = get_first_template_match(template_name)

    if not match:
        return

    x, y = match.rect.center
    adb.tap(x, y)


def wait_for_first_template_match(
        template_name: str,
        timeout: int | float = 60,
        check_interval: int | float | Callable[[int], float] = _default_check_interval_fn,
        raise_on_timeout: bool = False,
) -> bool:
    start_time = time.time()
    i = 0

    while True:
        sleep_duration = check_interval(i) if callable(check_interval) else check_interval
        time.sleep(sleep_duration)

        match = get_first_template_match(template_name)

        if match:
            return True

        if time.time() - start_time > timeout:
            if raise_on_timeout:
                raise TimeoutError(f"Timeout waiting for template match: {template_name}")
            return False

        i += 1
