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


# class GroupTeachersService(GroupTeachersServiceProtocol): # так же, как students, но пока вместо teachers у нас users; нужно создать apps/teachers
