from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.group_students import GroupStudentServiceProtocol


class DeleteStudentUseCaseProtocol(UseCaseProtocol[None]):
    async def __call__(self, group_id: UUID, student_id: UUID) -> None:
        ...


class DeleteStudentUseCase(DeleteStudentUseCaseProtocol):
    def __init__(self, student_service: GroupStudentServiceProtocol):
        self.student_service = student_service
    
    async def __call__(self, group_id: UUID, student_id: UUID) -> None:
        await self.student_service.delete_student(group_id, student_id) 