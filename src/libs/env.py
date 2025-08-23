import os
from dataclasses import dataclass

from src.libs.undefined import undefined, Undefined


@dataclass
class EnvironmentVariable:
    name: str
    default: str = undefined

    def get(self, default: str | Undefined = undefined) -> str:
        if self.name in os.environ:
            return os.environ[self.name]

        if default is not undefined:
            return default

        if self.default is not undefined:
            return self.default

        raise EnvironmentError(f"Environment variable '{self.name}' is not set and no default values provided.")



EnvVar = EnvironmentVariable
