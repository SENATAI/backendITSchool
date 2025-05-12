from typing import Self, List
from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.users.schemas import UserReadSchema
from school_site.apps.users.services.users import UserServiceProtocol

class DeleteUserUseCaseProtocol(UseCaseProtocol[bool]):
    async def __call__(self: Self, user_id: UUID) -> bool:
        ...

class DeleteUserUseCase(DeleteUserUseCaseProtocol):
    def __init__(self: Self, user_service: UserServiceProtocol):
        self.user_service = user_service

    async def __call__(self: Self, user_id: UUID) -> bool:
        return await self.user_service.delete_user(user_id)