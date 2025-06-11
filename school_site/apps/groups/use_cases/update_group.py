from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.groups import GroupServiceProtocol
from ..schemas import GroupReadSchema, GroupUpdateSchema

class UpdateGroupUseCaseProtocol(UseCaseProtocol[GroupReadSchema]):
    async def __call__(self, group_id: UUID, group_data: GroupUpdateSchema) -> GroupReadSchema:
        ...

class UpdateGroupUseCase(UpdateGroupUseCaseProtocol):
    def __init__(self, group_service: GroupServiceProtocol):
        self.group_service = group_service
    
    async def __call__(self, group_id: UUID, group_data: GroupUpdateSchema) -> GroupReadSchema:
        return await self.group_service.update(group_id, group_data) 