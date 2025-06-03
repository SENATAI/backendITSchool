from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.group_teachers import GroupTeacherServiceProtocol


class DeleteTeacherUseCaseProtocol(UseCaseProtocol[None]):
    async def __call__(self, group_id: UUID, teacher_id: UUID) -> None:
        ...


class DeleteTeacherUseCase(DeleteTeacherUseCaseProtocol):
    def __init__(self, teacher_service: GroupTeacherServiceProtocol):
        self.teacher_service = teacher_service
    
    async def __call__(self, group_id: UUID, teacher_id: UUID) -> None:
        await self.teacher_service.delete_teacher(group_id, teacher_id) 