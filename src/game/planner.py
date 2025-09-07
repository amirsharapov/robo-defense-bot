from dataclasses import dataclass
from pathlib import Path

from src.game.constants import GRID_N_ROWS, GRID_N_COLS


_plans_cache = {}


def get_plan(name: str) -> 'ExecutionPlan | None':
    global _plans_cache
    return _plans_cache.get(name)


def set_plan(name: str, plan: 'ExecutionPlan'):
    global _plans_cache
    if name in _plans_cache:
        raise ValueError(f"Plan with name {name} already exists in cache")
    _plans_cache[name] = plan


def clear_plans_cache():
    global _plans_cache
    _plans_cache = {}


@dataclass
class ExecutionPlan:
    name: str | None
    description: str | None
    final_grid_state: list[list[str | None]] | None
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
        'final_grid_state': [],
        'tile_update_order': []
    }

    current_section = None

    # tile update order specific context
    tile_update_order_visited = set()

    for line in file_contents.splitlines():
        if line.strip() == '':
            continue

        if line.strip().startswith('#'):
            continue

        if line.startswith('$ meta'):
            current_section = 'meta'
            continue

        if line.startswith('$ final_grid_state'):
            current_section = 'final_grid_state'
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

        if current_section == 'final_grid_state':
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
            plan['final_grid_state'].append(parts)
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

    return plan


def process_plan(parsed: dict):
    # validate final state
    assert len(parsed['final_grid_state']) == GRID_N_ROWS
    for row in parsed['final_grid_state']:
        assert len(row) == GRID_N_COLS

    # validate tile update order
    for tile in parsed['tile_update_order']:
        assert 'rows' in tile
        assert 'cols' in tile
        rows, cols = tile['rows'], tile['cols']
        assert len(rows) == 1 or len(cols) == 1, 'Cannot have both rows and cols be ranges'
        assert len(cols) in (1, 2)
        assert len(rows) in (1, 2)
        for r in rows:
            assert 0 <= r < GRID_N_ROWS
        for c in cols:
            assert 0 <= c < GRID_N_COLS

    plan = ExecutionPlan(
        name=parsed['meta']['name'],
        description=parsed['meta'].get('description'),
        final_grid_state=parsed['final_grid_state'],
        commands=[]
    )

    # expand tile update order
    tile_update_order_expanded = []
    visited = set()

    for tile in parsed['tile_update_order']:
        for key in ['rows', 'cols']:
            items = tile[key]
            if len(items) == 2:
                start, end = items
                step = 1 if start < end else -1
                tile[key] = list(range(start, end + step, step))
            else:
                tile[key] = items

        rows, cols = tile['rows'], tile['cols']

        for row in rows:
            for col in cols:
                tile_update_order_expanded.append((row, col))
                visited.add((row, col))

    # fill in remaining tiles in row-major order
    for row_i in range(GRID_N_ROWS):
        for col_i in range(GRID_N_COLS):
            if (row_i, col_i) not in visited:
                tile_update_order_expanded.append((row_i, col_i))
                visited.add((row_i, col_i))

    # iterate over expanded tile update order and generate commands
    if parsed['meta'].get('previous_plan'):
        previous_plan = get_plan(parsed['meta']['previous_plan'])
        previous_grid = previous_plan.final_grid_state
    else:
        previous_grid = [[None for _ in range(GRID_N_COLS)] for _ in range(GRID_N_ROWS)]

    for row_i, col_i in tile_update_order_expanded:
        previous_tower_id = previous_grid[row_i][col_i]
        tower_id = parsed['final_grid_state'][row_i][col_i]

        if tower_id is None:
            continue

        if previous_tower_id == tower_id:
            continue

        plan.commands.append(
            UpdateTileCommand(
                target_tower_id=tower_id,
                row_i=row_i,
                col_i=col_i
            )
        )

    return plan


def read_plan(path: str | Path):
    parsed = parse_plan(path)
    processed = process_plan(parsed)
    return processed


def get_plans_for_strategy(strategy: str) -> list[ExecutionPlan]:
    plans_dir = Path('data/src/plans') / strategy
    assert plans_dir.exists(), f"Plans directory {plans_dir} does not exist"
    assert plans_dir.is_dir(), f"Plans path {plans_dir} is not a directory"

    files = []
    for file in plans_dir.iterdir():
        files.append(int(file.name))

    files.sort()
    plans = []
    for file in files:
        file = plans_dir / str(file)
        plan = read_plan(file)
        set_plan(plan.name, plan)
        plans.append(plan)

    return plans
