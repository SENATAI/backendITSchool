from enum import Enum

class NewsStatus(str, Enum):
    LOW = 'low'
    HIGH = 'high'
    TOP = 'top'