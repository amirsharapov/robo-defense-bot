from src.game import controls, state
from src.game.controls import place_tower, upgrade_tower, tap_start_game_button, tap_new_game_button
from src.game.grid import AnchorTypes
from src.game.state import get_tile_grid, get_camera_position, CameraPositions, set_camera_position
from src.game.towers import get_tower
from src.game.vision import locate_exit_anchor


def update_camera_position_to_fit_row_on_screen(
        row_i: int
):
    camera_position = get_camera_position()

    threshold_top = 2
    threshold_bottom = 6

    if threshold_top < row_i < threshold_bottom:
        return

    if row_i <= threshold_top:
        if camera_position == CameraPositions.TOP:
            return

        controls.swipe('down')
        state.update_tile_grid_positions()
        set_camera_position(CameraPositions.TOP)
        return

    if row_i >= threshold_bottom:
        if camera_position == CameraPositions.BOTTOM:
            return

        controls.swipe('up')
        state.update_tile_grid_positions()
        set_camera_position(CameraPositions.BOTTOM)
        return

    print(f"Could not adjust camera for row {row_i}")


def update_tile(
        row_i: int,
        col_i: int,
        target_tower_id: str | None
):
    update_camera_position_to_fit_row_on_screen(row_i)

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


def start_new_game(level: int = 10):
    tap_new_game_button()
    tap_start_game_button()
