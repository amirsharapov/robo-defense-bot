from dataclasses import dataclass


@dataclass
class UpdateTileCommand:
    target_tower_id: str
    col_i: int
    row_i: int


def parse_plan() -> dict:
    pass


def read_plan():
    pass
