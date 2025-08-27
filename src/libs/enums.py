from enum import StrEnum


class BaseEnum(StrEnum):

    @staticmethod
    def _generate_next_value_(name: str, *args):
        return name.upper()

    @classmethod
    def _missing_(cls, value):
        value = str(value).upper()
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")
