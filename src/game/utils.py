from numpy import ndarray

from src import templates
from src.libs import android, vision, adb
from src.libs.utils import first_or_none


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
