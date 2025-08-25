from enum import auto

from src.libs.enums import BaseEnum
from src.libs.geometry import Rectangle


class AnchorTypes(BaseEnum):
    EXIT = auto()


def generate_grid(anchor: AnchorTypes, anchor_rect: Rectangle):
    assert anchor == AnchorTypes.EXIT, "Currently only EXIT anchor is supported"

    n_cols = 18
    n_rows = 10
    cell_w = 66
    cell_h = 66

    origin_x = anchor_rect.x - (n_cols * cell_w)
    origin_y = anchor_rect.y - (5 * cell_h)  # anchor is in the middle of the right edge

    matrix = []
    for row_i in range(n_rows):
        row = []
        for col_i in range(n_cols):
            tile_x = origin_x + (col_i * 66)
            tile_y = origin_y + (row_i * 66)
            row.append(
                Rectangle(
                    x=tile_x,
                    y=tile_y,
                    w=66,
                    h=66
                )
            )
        matrix.append(row)

    return matrix