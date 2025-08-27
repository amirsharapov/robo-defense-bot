import time

from src.game.client import get_tile_grid
from src.game.constants import (
    GUN_TOWER_POSITION,
    ROCKET_TOWER_POSITION,
    SLOW_TOWER_POSITION,
    FAST_FORWARD_POSITION,
    PAUSE_POSITION
)
from src.game.towers import get_tower
from src.game.vision import locate_start_game_button
from src.libs.adb import send_motion_event, MotionEvents, tap
from src.libs.android import screenshot
from src.libs.geometry import Line, Point


def place_tower(
        tile_row_index: int,
        tile_col_index: int,
        tower_id: str
):
    tower = get_tower(tower_id)

    assert tower.category_id in ('gu', 'ro', 'sl'), f"Cannot place tower of type {tower.category_id}"

    grid = get_tile_grid()
    tile = grid[tile_row_index][tile_col_index]

    tower_x, tower_y = {
        'gu': GUN_TOWER_POSITION,
        'ro': ROCKET_TOWER_POSITION,
        'sl': SLOW_TOWER_POSITION
    }[tower.category_id]

    line = Line(
        Point(tower_x, tower_y),
        tile.rect.center.translated(dy=50)
    )

    send_motion_event(
        MotionEvents.DOWN,
        line.point1.x,
        line.point1.y,
    )

    points = line.linspace(steps=5)
    for point in points:
        send_motion_event(
            MotionEvents.MOVE,
            int(point.x),
            int(point.y)
        )

    time.sleep(0.2)
    send_motion_event(
        MotionEvents.UP,
        line.point2.x,
        line.point2.y
    )

    time.sleep(0.2)


def upgrade_tower(
        tile_row_index: int,
        tile_col_index: int,
        source_tower_id: str,
        target_tower_id: str,
):
    grid = get_tile_grid()
    tile = grid[tile_row_index][tile_col_index]

    tower = get_tower(source_tower_id)

    upgrade_option = tower.get_upgrade_option(target_tower_id)
    assert upgrade_option is not None, f"Cannot upgrade from {source_tower_id} to {target_tower_id}"

    x, y = tile.rect.center
    tap(x, y)

    time.sleep(0.5)

    x, y = upgrade_option.position_xy
    tap(x, y)

    time.sleep(0.5)


def toggle_fast_forward_button():
    x, y = FAST_FORWARD_POSITION
    tap(x, y)


def toggle_pause_button():
    x, y = PAUSE_POSITION
    tap(x, y)


def adjust_screen():
    global _tile_grid
    _tile_grid = None


def start_game():
    image = screenshot()
    match = locate_start_game_button(image)

    if not match:
        print(f'Could not find start game button.')
        return

    tap(
        match.rect.x,
        match.rect.y
    )
