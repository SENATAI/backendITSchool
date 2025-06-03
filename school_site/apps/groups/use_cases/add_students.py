from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.group_students import GroupStudentServiceProtocol
from ..schemas import GroupAddStudentsSchema, GroupReadStudentsSchema


class AddStudentsUseCaseProtocol(UseCaseProtocol[GroupReadStudentsSchema]):
    async def __call__(self, group_id: UUID, students: GroupAddStudentsSchema) -> GroupReadStudentsSchema:
        ...


class AddStudentsUseCase(AddStudentsUseCaseProtocol):
    def __init__(self, group_student_service: GroupStudentServiceProtocol):
        self.group_student_service = group_student_service

    async def __call__(self, group_id: UUID, students: GroupAddStudentsSchema) -> GroupReadStudentsSchema:
        return await self.group_student_service.add_students(group_id, students) 