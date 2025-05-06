from enum import Enum

class AgeCategory(str, Enum):
    ALL = "All"
    SIX_PLUS = "SixPlus"
    TWELVE_PLUS = "TwelvePlus"