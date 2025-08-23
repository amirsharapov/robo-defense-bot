from enum import StrEnum


class BaseEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name: str, *args):
        return name.upper()