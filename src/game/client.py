import time

from src.game.constants import PAUSE_POSITION, GUN_TOWER_POSITION, ROCKET_TOWER_POSITION, SLOW_TOWER_POSITION, \
    FAST_FORWARD_POSITION, UPGRADE_GUN_TOWER_TO_2_POSITION, UPGRADE_GUN_TOWER_TO_3_POSITION
from src.game.enums import Towers, Upgrades
from src.game.grid import generate_grid, AnchorTypes
from src.game.vision import locate_exit_anchor, locate_start_game_button
from src.libs.adb import tap, swipe, send_motion_event, MotionEvents
from src.libs.android import screenshot
from src.libs.geometry import Rectangle, Line, Point

_grid: list[list[Rectangle]] | None = None


def get_grid():
    global _grid
    if not _grid:
        _grid = generate_grid(
            AnchorTypes.EXIT,
            locate_exit_anchor().rect
        )
    return _grid


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
    global _grid
    _grid = None


def toggle_pause_button():
    x, y = PAUSE_POSITION
    tap(x, y)


def toggle_fast_forward_button():
    x, y = FAST_FORWARD_POSITION
    tap(x, y)


def place_towers(place_tower_args: list[tuple[int, int, str | Towers]]):
    for tile_row_index, tile_col_index, tower_type in place_tower_args:
        place_tower(
            tile_row_index,
            tile_col_index,
            tower_type
        )


def place_tower(
        tile_row_index: int,
        tile_col_index: int,
        tower: str | Towers
):
    if isinstance(tower, str):
        tower = Towers(tower.upper())

    grid = get_grid()
    tile = grid[tile_row_index][tile_col_index]

    tower_x, tower_y = {
        Towers.GUN: GUN_TOWER_POSITION,
        Towers.ROCKET: ROCKET_TOWER_POSITION,
        Towers.SLOW: SLOW_TOWER_POSITION
    }[tower]

    start = Point(
        tower_x,
        tower_y
    )

    end = Point(
        tile.center.x,
        tile.center.y + 50
    )

    line = Line(start, end)

    send_motion_event(
        MotionEvents.DOWN,
        start.x,
        start.y,
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
        end.x,
        end.y
    )

    # TODO Store in memory tower is placed

    time.sleep(0.2)


def upgrade_towers(upgrade_tower_args: list[tuple[int, int, list[str | Upgrades]]]):
    for tile_row_index, tile_col_index, upgrades in upgrade_tower_args:
        upgrade_tower(
            tile_row_index,
            tile_col_index,
            upgrades
        )


def upgrade_tower(
        tile_row_index: int,
        tile_col_index: int,
        upgrades: list[str | Upgrades]
):
    for i, upgrade in enumerate(upgrades):
        if isinstance(upgrade, str):
            upgrades[i] = Upgrades(upgrade.upper())

    grid = get_grid()
    tile = grid[tile_row_index][tile_col_index]

    # TODO validate the tower type and current level

    for upgrade in upgrades:
        tap(
            tile.center.x,
            tile.center.y
        )

        time.sleep(0.5)

        upgrade_button_xy = {
            Upgrades.GUN_2: UPGRADE_GUN_TOWER_TO_2_POSITION,
            Upgrades.GUN_3: UPGRADE_GUN_TOWER_TO_3_POSITION
        }[upgrade]

        tap(
            upgrade_button_xy[0],
            upgrade_button_xy[1]
        )

        time.sleep(0.5)


def place_and_upgrade_tower(
        tile_row_index: int,
        tile_col_index: int,
        tower: str | Towers,
        upgrades: list[str | Upgrades]
):
    place_tower(
        tile_row_index,
        tile_col_index,
        tower
    )

    if upgrades:
        upgrade_tower(
            tile_row_index,
            tile_col_index,
            upgrades
        )


def place_and_upgrade_towers(
        place_and_upgrade_tower_args: list[tuple[int, int, str | Towers, list[str | Upgrades]]]
):
    for tile_row_index, tile_col_index, tower_type, upgrades in place_and_upgrade_tower_args:
        place_and_upgrade_tower(
            tile_row_index,
            tile_col_index,
            tower_type,
            upgrades
        )