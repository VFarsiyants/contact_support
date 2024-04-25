from enum import Enum


class ContactLevelEnum(Enum):
    """Contact level enums"""
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"


def enum_values(enum_class):
    return [e.value for e in enum_class]
