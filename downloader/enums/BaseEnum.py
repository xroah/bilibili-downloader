from enum import Enum


class BaseEnum(Enum):
    def __str__(self) -> str:
        return self.value
