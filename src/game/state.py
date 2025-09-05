from enum import auto

from src.game import grid
from src.game.grid import GridTile, generate_tile_grid, AnchorTypes
from src.game.vision import locate_exit_anchor
from src.libs.enums import BaseEnum

_tile_grid: list[list['GridTile']] | None = None
_camera_position: 'CameraPositions | None' = None


class CameraPositions(BaseEnum):
    DEFAULT = auto()
    TOP = auto()
    BOTTOM = auto()


def get_tile_grid():
    global _tile_grid
    anchor = locate_exit_anchor()

    if not _tile_grid:
        _tile_grid = generate_tile_grid(
            AnchorTypes.EXIT,
            anchor.rect
        )

    return _tile_grid


def update_tile_grid_positions():
    global _tile_grid
    anchor = locate_exit_anchor()

    if not _tile_grid:
        print("Tile grid has not been initialized yet.")
        return

    if not anchor:
        print("Could not find exit anchor to update tile grid positions.")
        return

    grid.update_tile_grid_positions(
        _tile_grid,
        AnchorTypes.EXIT,
        anchor.rect
    )


def get_camera_position() -> 'CameraPositions':
    global _camera_position
    return _camera_position


def set_camera_position(position: 'CameraPositions'):
    global _camera_position
    _camera_position = position
