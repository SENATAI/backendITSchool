from typing import Self
from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.users.schemas import UserReadSchema
from school_site.apps.users.services.users import UserServiceProtocol

class GetUserByIdUseCaseProtocol(UseCaseProtocol[UserReadSchema]):
    async def __call__(self: Self, user_id: UUID) -> UserReadSchema:
        ...

class GetUserByIdUseCase(GetUserByIdUseCaseProtocol):
    def __init__(self: Self, user_service: UserServiceProtocol):
        self.user_service = user_service

    async def __call__(self: Self, user_id: UUID) -> UserReadSchema:
        return await self.user_service.get_user_by_id(user_id)
        
