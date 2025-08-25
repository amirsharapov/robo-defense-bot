from pathlib import Path


def get_data_path() -> Path:
    return Path('data')


def get_local_path() -> Path:
    return Path('local')


def get_templates_path() -> Path:
    return get_data_path() / 'src/templates'


def get_logs_dir() -> Path:
    return get_local_path() / 'logs'