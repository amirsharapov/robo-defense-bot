from enum import auto

from src.game import grid, utils
from src.game.grid import GridTile, generate_tile_grid, AnchorTypes
from src.libs.enums import BaseEnum
from src.libs.logging import get_logger

_tile_grid: list[list['GridTile']] | None = None
_camera_position: 'CameraPositions | None' = None
_is_paused: bool = False
_is_fast_forward: bool = False

logger = get_logger(__name__)

class CameraPositions(BaseEnum):
    DEFAULT = auto()
    TOP = auto()
    BOTTOM = auto()


def locate_exit_anchor():
    logger.info("Locating exit anchor on the screen")
    return utils.get_first_template_match('game/basic_level/anchor.png')


def get_tile_grid():
    global _tile_grid

    if not _tile_grid:
        anchor = locate_exit_anchor()
        _tile_grid = generate_tile_grid(
            AnchorTypes.EXIT,
            anchor.rect
        )

    return _tile_grid


def set_tile_grid(tile_grid):
    global _tile_grid
    _tile_grid = tile_grid


def refresh_tile_grid_positions():
    global _tile_grid
    anchor = locate_exit_anchor()

    if not _tile_grid:
        print("Tile grid has not been initialized yet.")
        return

    if not anchor:
        print("Could not find exit anchor to update tile grid positions.")
        return

    grid.update_existing_tile_grid_rects(
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


def is_paused() -> bool:
    global _is_paused
    return _is_paused


def set_paused(paused: bool):
    global _is_paused
    _is_paused = paused


def is_fast_forward_enabled() -> bool:
    global _is_fast_forward
    return _is_fast_forward


def set_fast_forward(fast_forward: bool):
    global _is_fast_forward
    _is_fast_forward = fast_forward


def reset():
    set_fast_forward(False)
    set_paused(False)
    set_camera_position(CameraPositions.DEFAULT)
    set_tile_grid(None)
