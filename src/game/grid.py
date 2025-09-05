from dataclasses import dataclass
from enum import auto

from src.game.towers import get_tower
from src.libs.enums import BaseEnum
from src.libs.geometry import Rectangle


class AnchorTypes(BaseEnum):
    EXIT = auto()


@dataclass
class GridTile:
    rect: Rectangle
    tower_id: str | None

    @property
    def tower(self):
        return get_tower(self.tower_id)


def update_tile_grid_positions(grid: list[list[GridTile]], anchor_type: AnchorTypes, anchor_rect: Rectangle):
    assert anchor_type == AnchorTypes.EXIT, "Currently only EXIT anchor is supported"

    new_grid = generate_tile_grid(
        anchor_type,
        anchor_rect
    )

    for row_i, row in enumerate(grid):
        for col_i, tile in enumerate(row):
            tile.rect.overwrite(new_grid[row_i][col_i].rect)


def generate_tile_grid(anchor_type: AnchorTypes, anchor_rect: Rectangle):
    assert anchor_type == AnchorTypes.EXIT, "Currently only EXIT anchor is supported"

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
                GridTile(
                    rect=Rectangle(
                        x=tile_x,
                        y=tile_y,
                        w=66,
                        h=66
                    ),
                    tower_id=None
                )
            )
        matrix.append(row)

    return matrix
