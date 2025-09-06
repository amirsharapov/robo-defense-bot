import time

from src.game import state
from src.game.constants import (
    GUN_TOWER_POSITION,
    ROCKET_TOWER_POSITION,
    SLOW_TOWER_POSITION, FAST_FORWARD_POSITION, PAUSE_POSITION
)
from src.game.state import (
    get_tile_grid,
    get_camera_position,
    CameraPositions,
    set_camera_position
)
from src.game.towers import get_tower
from src.game.utils import get_first_template_match
from src.libs import android, adb
from src.libs.geometry import Line, Point


def update_tiles(list_of_args: list[tuple]):
    for row_i, col_i, target_tower_id in list_of_args:
        update_tile(
            row_i,
            col_i,
            target_tower_id
        )


def update_tile(
        row_i: int,
        col_i: int,
        target_tower_id: str | None
):
    update_camera_position_to_fit_row_on_screen(row_i)

    tiles = get_tile_grid()
    existing_tower = tiles[row_i][col_i].tower
    target_tower = get_tower(target_tower_id)

    upgrade_path = target_tower.upgrade_path

    if existing_tower is None:
        first_tower = upgrade_path[0]
        purchase_tower(
            row_i,
            col_i,
            first_tower.id
        )
        current_tower = first_tower
        upgrade_i = 0
        tiles[row_i][col_i].tower_id = first_tower.id

    else:
        assert existing_tower in upgrade_path, f"Cannot upgrade from {existing_tower.id} to {target_tower.id}"
        current_tower = existing_tower
        upgrade_i = upgrade_path.index(existing_tower)

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


def purchase_tower(
        row_i: int,
        col_i: int,
        tower_id: str
):
    tower = get_tower(tower_id)

    assert tower.category_id in ('gu', 'ro', 'sl'), f"Cannot place tower of type {tower.category_id}"

    grid = get_tile_grid()
    tile = grid[row_i][col_i]

    tower_x, tower_y = {
        'gu': GUN_TOWER_POSITION,
        'ro': ROCKET_TOWER_POSITION,
        'sl': SLOW_TOWER_POSITION
    }[tower.category_id]

    line = Line(
        Point(tower_x, tower_y),
        tile.rect.center.translated(dy=50)
    )

    android.swipe_using_motion_events(
        line.point1.x,
        line.point1.y,
        line.point2.x,
        line.point2.y,
        steps=5
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
    adb.tap(x, y)

    time.sleep(0.5)

    print('Checking if upgrade is available...')
    match = None
    while match is None:
        match = get_first_template_match(f'game/tower_upgrades/{upgrade_option.target_tower_id}.png')
        if match is not None:
            print('Upgrade is available!')
            break
        print('Upgrade not available yet, waiting...')
        time.sleep(1)

    x, y = upgrade_option.position_xy
    adb.tap(x, y)

    time.sleep(0.5)


def update_camera_position_to_fit_row_on_screen(
        row_i: int
):
    camera_position = get_camera_position()

    threshold_top = 2
    threshold_bottom = 7

    if threshold_top < row_i < threshold_bottom:
        return

    if row_i <= threshold_top:
        if camera_position == CameraPositions.TOP:
            return

        android.swipe_towards_direction('down')
        state.refresh_tile_grid_positions()
        set_camera_position(CameraPositions.TOP)
        return

    if row_i >= threshold_bottom:
        if camera_position == CameraPositions.BOTTOM:
            return

        android.swipe_towards_direction('up')
        state.refresh_tile_grid_positions()
        set_camera_position(CameraPositions.BOTTOM)
        return

    raise Exception(f"Could not adjust camera for row {row_i}")


def enable_fast_forward():
    if not state.is_fast_forward_enabled():
        android.tap_point(FAST_FORWARD_POSITION)


def disable_fast_forward():
    if state.is_fast_forward_enabled():
        android.tap_point(FAST_FORWARD_POSITION)


def pause_game():
    if not state.is_paused():
        android.tap_point(PAUSE_POSITION)


def unpause_game():
    if state.is_paused():
        android.tap_point(PAUSE_POSITION)
