from dataclasses import dataclass
from pathlib import Path


@dataclass
class TemporaryFile:
    path: Path

    def create(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch()

    def delete(self):
        if self.path.exists():
            self.path.unlink()

    def __enter__(self):
        self.create()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()
