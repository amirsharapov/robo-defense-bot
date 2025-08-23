from enum import auto

from src.libs.enums import BaseEnum
from src.libs.shapes import Rectangle


class AnchorTypes(BaseEnum):
    EXIT = auto()


def generate_grid(anchor: AnchorTypes, rectangle: Rectangle):
    assert anchor == AnchorTypes.EXIT, "Currently only EXIT anchor is supported"

    n_cols = 18
    n_rows = 10
    cell_w = 66
    cell_h = 66

    origin_x = rectangle.x - (n_cols * cell_w)
    origin_y = rectangle.y - (5 * cell_h)  # anchor is in the middle of the right edge

    matrix = []
    for col_i in range(n_cols):
        col = []
        for row_i in range(n_rows):
            cell_x = origin_x + (col_i * 66)
            cell_y = origin_y + (row_i * 66)
            col.append(
                Rectangle(
                    x=cell_x,
                    y=cell_y,
                    w=66,
                    h=66
                )
            )
        matrix.append(col)

    return matrix