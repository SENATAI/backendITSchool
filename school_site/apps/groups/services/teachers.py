import logging
from typing import Protocol
from uuid import UUID
from ..schemas import (
    GroupAddTeacherSchema,
    GroupAddTeacherDBSchema,
    GroupReadSchema
)
from ..repositories.groups import GroupRepositoryProtocol


logger = logging.getLogger(__name__)


# class GroupTeachersServiceProtocol(Protocol):


# class GroupTeachersService(GroupTeachersServiceProtocol):
