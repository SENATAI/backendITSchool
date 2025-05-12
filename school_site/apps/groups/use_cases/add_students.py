from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.students import GroupStudentServiceProtocol
from ..schemas import GroupAddStudentsSchema


class AddStudentsUseCaseProtocol(UseCaseProtocol[None]):
    async def __call__(self, group_id: UUID, students: GroupAddStudentsSchema) -> None:
        ...


class AddStudentsUseCase(AddStudentsUseCaseProtocol):
    def __init__(self, student_service: GroupStudentServiceProtocol):
        self.student_service = student_service
    
    async def __call__(self, group_id: UUID, students: GroupAddStudentsSchema) -> None:
        await self.student_service.add_students(group_id, students) 