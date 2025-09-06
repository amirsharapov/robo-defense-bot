from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExecutionPlan:
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

    for line in file_contents.splitlines():
        if line.strip() == '':
            continue

        if line.startswith('$ final_state'):
            current_section = 'final_state'
            continue

        if line.startswith('$ meta'):
            current_section = 'meta'
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

        if current_section == 'final_state':
            # skip the header line
            if line == '   .0  .1  .2  .3  .4  .5  .6  .7  .8  .9  .10 .11 .12 .13 .14 .15 .16 .17 .':
                continue

            # remove the first 4 chars for row index and space
            line = line[4:].strip()
            parts = line.split('.')
            parts = parts[:-1]  # remove the trailing '.'
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
                start = int(start)
                end = int(end)
                reverse = end < start
                if reverse:
                    start, end = end, start
                if reverse:
                    rows = list(range(int(end), int(start) - 1, -1))
                else:
                    rows = list(range(int(start), int(end) + 1))
            else:
                rows = [int(rows)]

            line = line.split(' ', 1)[1].strip()
            line = line.removeprefix('col:')
            cols = line.split(' ')[0].strip()

            if '-' in cols:
                start, end = cols.split('-')
                start = int(start)
                end = int(end)
                reverse = end < start
                if reverse:
                    start, end = end, start
                if reverse:
                    cols = list(range(int(end), int(start) - 1, -1))
                else:
                    cols = list(range(int(start), int(end) + 1))
            else:
                cols = [int(cols)]

            if len(rows) > 1 and len(cols) > 1:
                raise ValueError("Cannot have both rows and cols be ranges")

            for r in rows:
                for c in cols:
                    plan['tile_update_order'].append({'row': r, 'col': c})

            continue

    return plan


def read_plan(path: str | Path):
    parsed = parse_plan(path)
    print(parsed)
