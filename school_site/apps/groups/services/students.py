import logging
from typing import Protocol
from uuid import UUID
from ..schemas import (
    GroupAddStudentsSchema,
    GroupAddStudentsDBSchema,
    GroupReadSchema
)
from ..repositories.groups import GroupRepositoryProtocol


logger = logging.getLogger(__name__)


# class GroupStudentsServiceProtocol(Protocol):


# class GroupStudentsService(GroupStudentsServiceProtocol):  # подтягивает сервис groups и уже существующий apps/students/services/students, с ними работает. если надо расширить apps/students/services/students там расширяешь, создав внизу новый класс, наследующийся от него
