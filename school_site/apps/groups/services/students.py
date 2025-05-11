import logging
from typing import Protocol
from uuid import UUID
from psycopg2.errors import ForeignKeyViolation
from school_site.apps.students.services.students import StudentServiceProtocol
from ..repositories.group_students import GroupStudentsRepositoryProtocol
from ..schemas import GroupAddStudentsSchema, GroupAddStudentsDBSchema

logger = logging.getLogger(__name__)


class GroupStudentServiceProtocol(Protocol):
    async def add_students(self, group_id: UUID, students: GroupAddStudentsSchema) -> None:
        ...

    async def delete_student(self, group_id: UUID, student_id: UUID) -> None:
        ...


class GroupStudentService(GroupStudentServiceProtocol):
    def __init__(
        self,
        group_students_repository: GroupStudentsRepositoryProtocol,
        student_service: StudentServiceProtocol
    ):
        self.group_students_repository = group_students_repository
        self.student_service = student_service

    async def add_students(self, group_id: UUID, students: GroupAddStudentsSchema) -> None:
        try:
            students_db = GroupAddStudentsDBSchema(students_id=students.students_id)
            await self.group_students_repository.add_students(group_id, students_db)
        except ForeignKeyViolation as e:
            logger.error(f"Error adding students to group: {str(e)}")
            raise ValueError("One or more students not found or group not found")

    async def delete_student(self, group_id: UUID, student_id: UUID) -> None:
        try:
            await self.group_students_repository.delete_student(group_id, student_id)
        except ForeignKeyViolation as e:
            logger.error(f"Error deleting student from group: {str(e)}")
            raise ValueError("Student or group not found")
