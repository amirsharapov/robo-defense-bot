from dataclasses import dataclass
from pathlib import Path

from src.game.constants import GRID_N_ROWS, GRID_N_COLS


@dataclass
class ExecutionPlan:
    name: str | None
    description: str | None
    commands: list['UpdateTileCommand']


@dataclass
class UpdateTileCommand:
    target_tower_id: str
    col_i: int
    row_i: int


def parse_plan(path: str | Path) -> dict:
    path = Path(path)
    file_contents = path.read_text().strip()

    plan = {
        'meta': {},
        'final_state': [],
        'tile_update_order': []
    }

    current_section = None

    # tile update order specific context
    tile_update_order_visited = set()

    for line in file_contents.splitlines():
        if line.strip() == '':
            continue

        if line.startswith('$ meta'):
            current_section = 'meta'
            continue

        if line.startswith('$ final_state'):
            current_section = 'final_state'
            continue

        if line.startswith('$ tile_update_order'):
            current_section = 'tile_update_order'
            continue

        if current_section == 'meta':
            if line.startswith('- name:'):
                name = line.removeprefix('- name:').strip()
                plan['meta']['name'] = name
                continue
            if line.startswith('- description:'):
                author = line.removeprefix('- description:').strip()
                plan['meta']['description'] = author
                continue
            if line.startswith('- previous_plan:'):
                previous_plan = line.removeprefix('- previous_plan:').strip()
                plan['meta']['previous_plan'] = None if previous_plan == 'null' else previous_plan
                continue

        if current_section == 'final_state':
            # skip the header line
            if line == '   .0  .1  .2  .3  .4  .5  .6  .7  .8  .9  .10 .11 .12 .13 .14 .15 .16 .17 .':
                continue

            # remove the first 4 chars for row index and space
            line = line[4:].strip()
            parts = line.split('.')
            parts = parts[:-1]  # remove the trailing '.'
            assert len(parts) == GRID_N_COLS

            parts = [p.removeprefix('.').removesuffix('.').strip() for p in parts]
            parts = [p if p != '' else None for p in parts]
            plan['final_state'].append(parts)
            continue

        if current_section == 'tile_update_order':
            if not line.startswith('- '):
                continue

            line = line.removeprefix('- ').strip()
            line = line.removeprefix('row:')
            rows = line.split(' ')[0].strip()

            if '-' in rows:
                start, end = rows.split('-')
                rows = [int(start), int(end)]
            else:
                rows = [int(rows)]

            line = line.split(' ', 1)[1].strip()
            line = line.removeprefix('col:')
            cols = line.split(' ')[0].strip()

            if '-' in cols:
                start, end = cols.split('-')
                cols = [int(start), int(end)]
            else:
                cols = [int(cols)]

            plan['tile_update_order'].append({'rows': rows, 'cols': cols})
            continue

    assert len(plan['final_state']) == GRID_N_ROWS

    # filter tile order if no tower is placed in final state. NEED to be done after linking previous plan for diffs.

    return plan


def process_plan(parsed: dict):
    # validate final state
    assert len(parsed['final_state']) == GRID_N_ROWS
    for row in parsed['final_state']:
        assert len(row) == GRID_N_COLS

    # validate tile update order
    for tile in parsed['tile_update_order']:
        assert 'rows' in tile
        assert 'cols' in tile
        rows, cols = tile['rows'], tile['cols']
        assert len(rows) == 1 or len(rows) == 1, 'Cannot have both rows and cols be ranges'

    plan = ExecutionPlan(
        name=None,
        description=None,
        commands=[]
    )

    # todo replace final state cells with Tower objects instead of tower ids
    # todo generate diffs between current plan and previous plan final state (if prev plan exists)
    # todo expand tile update order
    # todo generate `update_tile` commands from tile update order and the diffs

    return plan


def read_plan(path: str | Path):
    parsed = parse_plan(path)
    processed = process_plan(parsed)
    return processed
