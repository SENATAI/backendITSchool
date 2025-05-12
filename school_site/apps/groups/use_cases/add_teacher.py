from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.teachers import GroupTeacherServiceProtocol
from ..schemas import GroupAddTeacherSchema


class AddTeacherUseCaseProtocol(UseCaseProtocol[None]):
    async def __call__(self, group_id: UUID, teacher: GroupAddTeacherSchema) -> None:
        ...


class AddTeacherUseCase(AddTeacherUseCaseProtocol):
    def __init__(self, teacher_service: GroupTeacherServiceProtocol):
        self.teacher_service = teacher_service
    
    async def __call__(self, group_id: UUID, teacher: GroupAddTeacherSchema) -> None:
        await self.teacher_service.add_teacher(group_id, teacher) 