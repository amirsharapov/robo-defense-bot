from pathlib import Path


def get_data_path() -> Path:
    return Path('data')


def get_templates_path() -> Path:
    return get_data_path() / 'src/templates'