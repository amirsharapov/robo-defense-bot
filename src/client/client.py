from src.client.enums import TowerTypes
from src.client.grid import AnchorTypes, generate_grid
from src.client.vision import locate_exit_anchor

_data = {
    'grid': None
}


def get_grid():
    if _data['grid'] is None:
        rect = locate_exit_anchor()
        _data['grid'] = generate_grid(
            anchor=AnchorTypes.EXIT,
            rectangle=rect
        )
    return _data['grid']


def place_tower(
        col_index: int,
        row_index: int,
        tower_type: TowerTypes
):
    grid = get_grid()