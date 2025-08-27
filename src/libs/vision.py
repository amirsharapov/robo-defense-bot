from dataclasses import dataclass

import numpy as np
import cv2

from src.libs.geometry import Rectangle


def get_mask(image: np.ndarray):
    assert image.shape[2] == 4, "Image must have an alpha channel (shape[2] == 4)"
    mask = image[:, :, 3]
    mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)[1]
    return mask


def convert_bgr_to_gray(image: np.ndarray):
    assert len(image.shape) in (3, 4), "Image must have 3 or 4 channels"
    method = {
        3: cv2.COLOR_BGR2GRAY,
        4: cv2.COLOR_BGRA2GRAY,
    }
    return cv2.cvtColor(image, method[len(image.shape)])


@dataclass
class TemplateMatchResult:
    rectangle: Rectangle
    confidence: float | None

    @property
    def rect(self):
        return self.rectangle


def match_template(
        image: np.ndarray,
        template: np.ndarray,
        threshold: float = 0.9,
        use_mask: np.ndarray | None = None,
        method: int = cv2.TM_CCOEFF_NORMED,
        region: Rectangle | None = None,
        convert_image_to_gray: bool = True,
        convert_template_to_gray: bool = True,
        group_rectangles: bool = True
) -> list[TemplateMatchResult]:
    assert len(image.shape) >= 3, "Image must have at least 3 channels"

    # make a copy to avoid modifying the original image
    image = image.copy()

    # if we use mask, create the mask and image have 4 channels
    if use_mask:
        mask = get_mask(template)
        if template.shape[2] == 3:
            template = cv2.cvtColor(template, cv2.COLOR_BGR2BGRA)
    else:
        mask = None

    # grayscale is known to work better for template matching. Convert unless specified otherwise
    if convert_image_to_gray:
        image = convert_bgr_to_gray(image)
    if convert_template_to_gray:
        template = convert_bgr_to_gray(template)

    # check if template size is greater than image
    h, w = template.shape[:2]
    if h > image.shape[0] or w > image.shape[1]:
        return []

    # define the search space
    if region:
        x1, y1, x2, y2 = region.to_xyxy()
        search_space = image[y1:y2, x1:x2]
    else:
        search_space = image

    result = cv2.matchTemplate(
        search_space,
        template,
        method,
        None,
        mask
    )

    result = np.where(np.isfinite(result), result, 0)

    locations = np.where(result >= threshold)

    matches = []
    rects = []

    for point in zip(*locations[::-1]):
        confidence = result[point[1], point[0]]

        # adjust point if region is specified
        if region:
            point = (
                point[0] + region.x,
                point[1] + region.y
            )

        # if grouping enabled, add to list of rectangles. else add directly to matches
        # todo implement grouping while retaining confidence scores
        rect = Rectangle(
            x=point[0],
            y=point[1],
            w=w,
            h=h
        )

        if group_rectangles:
            rects.append(rect)

        else:
            matches.append(
                TemplateMatchResult(
                    rectangle=rect,
                    confidence=float(confidence)
                )
            )

    if not group_rectangles:
        return matches

    # normalize rectangles for grouping
    rects = [[r.x, r.y, r.w, r.h] for r in rects]

    if len(rects) > 1:
        rects, _ = cv2.groupRectangles(rects, groupThreshold=1, eps=0.3)

    for (x, y, w, h) in rects:
        rect = Rectangle(x=x, y=y, w=w, h=h)
        matches.append(
            TemplateMatchResult(
                rectangle=rect,
                confidence=None
            )
        )

    return matches
