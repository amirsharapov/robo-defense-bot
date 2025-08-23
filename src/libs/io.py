import uuid
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TemporaryFile:
    path: Path

    @classmethod
    def random_filename(cls, suffix: str | None = None) -> 'TemporaryFile':
        filename = str(uuid.uuid4())
        if suffix:
            filename += suffix
        return cls(Path(filename))

    def create(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch()
        return self

    def delete(self):
        if self.path.exists():
            self.path.unlink()

    def __enter__(self):
        return self.create()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.delete()
