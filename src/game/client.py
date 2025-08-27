from src.game.controls import place_tower, upgrade_tower
from src.game.grid import GridTile, generate_tile_grid, AnchorTypes
from src.game.towers import get_tower
from src.game.vision import locate_exit_anchor


_tile_grid: list[list['GridTile']] | None = None


def get_tile_grid():
    global _tile_grid

    anchor = locate_exit_anchor()

    if not _tile_grid:
        src.game.client._tile_grid = generate_tile_grid(
            AnchorTypes.EXIT,
            anchor.rect
        )

    return _tile_grid


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
