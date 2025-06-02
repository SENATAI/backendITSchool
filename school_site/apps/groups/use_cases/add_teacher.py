from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.group_teachers import GroupTeacherServiceProtocol
from ..schemas import GroupReadTeacherSchema


class AddTeacherUseCaseProtocol(UseCaseProtocol[GroupReadTeacherSchema]):
    async def __call__(self, group_id: UUID, teacher_id: UUID) -> GroupReadTeacherSchema:
        ...


class AddTeacherUseCase(AddTeacherUseCaseProtocol):
    def __init__(self, teacher_service: GroupTeacherServiceProtocol):
        self.teacher_service = teacher_service
    
    async def __call__(self, group_id: UUID, teacher_id: UUID) -> GroupReadTeacherSchema:
        return await self.teacher_service.add_teacher(group_id, teacher_id) 