import logging
from school_site.apps.groups.services.groups import GroupServiceProtocol
from typing import Protocol
from uuid import UUID
from sqlalchemy.exc import IntegrityError
from school_site.apps.students.services.students import StudentServiceProtocol
from ..repositories.group_students import GroupStudentsRepositoryProtocol
from ..schemas import GroupAddStudentsSchema, GroupAddStudentsDBSchema, GroupReadStudentsSchema
from school_site.core.utils.exceptions import ModelNotFoundException
from school_site.apps.students.models import Student

logger = logging.getLogger(__name__)


class GroupStudentServiceProtocol(Protocol):
    async def add_students(self, group_id: UUID, students: GroupAddStudentsSchema) -> GroupReadStudentsSchema:
        ...

    async def delete_student(self, group_id: UUID, student_id: UUID) -> bool:
        ...


class GroupStudentService(GroupStudentServiceProtocol):
    def __init__(
        self,
        group_students_repository: GroupStudentsRepositoryProtocol,
        group_service: GroupServiceProtocol,
        student_service: StudentServiceProtocol
    ):
        self.group_students_repository = group_students_repository
        self.group_service = group_service
        self.student_service = student_service

    async def add_students(self, group_id: UUID, students: GroupAddStudentsSchema) -> GroupReadStudentsSchema:
        group = await self.group_service.get(group_id)
        try:
            students_db = GroupAddStudentsDBSchema(students_id=students.students_id)
            await self.group_students_repository.add_students(group_id, students_db)
            return GroupReadStudentsSchema(
                id=group.id,
                name=group.name,
                description=group.description,
                start_date=group.start_date,
                end_date=group.end_date,
                students_id=students.students_id
            )
        except IntegrityError as e:
            logger.error(f"Error adding students to group: {str(e)}")
            raise ModelNotFoundException(
                model=Student,
                model_id=students.students_id
            )

    async def delete_student(self, group_id: UUID, student_id: UUID) -> bool:
        await self.group_students_repository.delete_student(group_id, student_id)
        return True