from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.groups import GroupServiceProtocol

class DeleteGroupUseCaseProtocol(UseCaseProtocol[None]):
    async def __call__(self, group_id: UUID) -> None:
        ...

class DeleteGroupUseCase(DeleteGroupUseCaseProtocol):
    def __init__(self, group_service: GroupServiceProtocol):
        self.group_service = group_service
    
    async def __call__(self, group_id: UUID) -> None:
        return await self.group_service.delete(group_id) 