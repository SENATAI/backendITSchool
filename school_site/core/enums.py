from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    ADMINISTRATOR = "administrator"