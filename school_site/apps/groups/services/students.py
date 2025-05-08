import logging
from typing import Protocol
from uuid import UUID
from school_site.apps.students.services.students import StudentServiceProtocol
from school_site.apps.groups.services.groups import GroupServiceProtocol
from ..schemas import GroupAddStudentsSchema

logger = logging.getLogger(__name__)


class GroupStudentServiceProtocol(Protocol):
    async def add_students(self, group_id: UUID, students: GroupAddStudentsSchema) -> None:
        ...

    async def delete_student(self, group_id: UUID, student_id: UUID) -> None:
        ...


class GroupStudentService(GroupStudentServiceProtocol):
    def __init__(
        self,
        group_service: GroupServiceProtocol,
        student_service: StudentServiceProtocol
    ):
        self.group_service = group_service
        self.student_service = student_service

    async def add_students(self, group_id: UUID, students: GroupAddStudentsSchema) -> None:
        for student_id in students.students_id:
            await self.student_service.get(student_id)
        await self.group_service.add_students(group_id, students)

    async def delete_student(self, group_id: UUID, student_id: UUID) -> None:
        await self.student_service.get(student_id)
        await self.group_service.delete_student(group_id, student_id)
