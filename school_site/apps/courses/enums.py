from enum import Enum

class AgeCategory(str, Enum):
    ALL_AGES = "All"
    FIVE_TO_SEVEN = "5-7"
    EIGHT_TO_TEN = "8-10"
    TWELVE_TO_FOURTEEN = "12-14"