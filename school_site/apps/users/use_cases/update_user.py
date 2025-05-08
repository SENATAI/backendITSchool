from typing import Self
from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.users.schemas import UserReadSchema, UserUpdateSchema
from school_site.apps.users.services.users import UserServiceProtocol

class UpdateUserUseCaseProtocol(UseCaseProtocol[UserReadSchema]):
    async def __call__(self: Self, user_id: UUID, user_data: UserUpdateSchema) -> UserReadSchema:
        ...

class UpdateUserUseCase(UpdateUserUseCaseProtocol):
    def __init__(self: Self, user_service: UserServiceProtocol):
        self.user_service = user_service

    async def __call__(self: Self, user_id: UUID, user_data: UserUpdateSchema) -> UserReadSchema:
        return await self.user_service.update_user(user_id, user_data)