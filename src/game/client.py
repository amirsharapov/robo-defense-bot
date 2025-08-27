import time
from dataclasses import dataclass

from src.game.constants import PAUSE_POSITION, GUN_TOWER_POSITION, ROCKET_TOWER_POSITION, SLOW_TOWER_POSITION, \
    FAST_FORWARD_POSITION, UPGRADE_GUN_TOWER_TO_2_POSITION, UPGRADE_GUN_TOWER_TO_3_POSITION
from src.game.grid import generate_grid, AnchorTypes, GridTile
from src.game.towers import get_tower
from src.game.vision import locate_exit_anchor, locate_start_game_button
from src.libs.adb import tap, send_motion_event, MotionEvents
from src.libs.android import screenshot
from src.libs.geometry import Line, Point

# used to store the grid of tiles and associated towers in memory
_tile_grid: list[list[GridTile]] | None = None


def get_tile_grid():
    global _tile_grid

    anchor = locate_exit_anchor()

    if not _tile_grid:
        _tile_grid = generate_grid(
            AnchorTypes.EXIT,
            anchor.rect
        )

    return _tile_grid


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


def adjust_screen():
    global _tile_grid
    _tile_grid = None


def toggle_pause_button():
    x, y = PAUSE_POSITION
    tap(x, y)


def toggle_fast_forward_button():
    x, y = FAST_FORWARD_POSITION
    tap(x, y)


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


def update_tile(
        row_i: int,
        col_i: int,
        target_tower_id: str | None
):
    tiles = get_tile_grid()
    source_tower = tiles[row_i][col_i].tower
    target_tower = get_tower(target_tower_id)

    upgrade_path = target_tower.upgrade_path

    if source_tower is None:
        first_tower = upgrade_path[0]
        place_tower(
            row_i,
            col_i,
            first_tower.id
        )
        current_tower = first_tower
        upgrade_i = 0
        tiles[row_i][col_i].tower_id = first_tower.id

    else:
        assert source_tower in upgrade_path, f"Cannot upgrade from {source_tower.id} to {target_tower.id}"
        current_tower = source_tower
        upgrade_i = upgrade_path.index(source_tower)

    upgrade_path = upgrade_path[upgrade_i + 1:]

    if not upgrade_path:
        return

    for tower in upgrade_path:
        upgrade_tower(
            row_i,
            col_i,
            current_tower.id,
            tower.id
        )
        tiles[row_i][col_i].tower_id = tower.id
        current_tower = tower


def update_tiles(list_of_args: list[tuple]):
    for row_i, col_i, target_tower_id in list_of_args:
        update_tile(
            row_i,
            col_i,
            target_tower_id
        )
