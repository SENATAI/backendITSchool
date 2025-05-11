from typing import Self
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.users.schemas import RegisterRequestSchema, UserReadSchema
from school_site.apps.users.services.users import UserServiceProtocol

class CreateUserUseCaseProtocol(UseCaseProtocol[UserReadSchema]):
    async def __call__(self: Self, user_data: RegisterRequestSchema) -> UserReadSchema:
        ...

class CreateUserUseCase(CreateUserUseCaseProtocol):
    def __init__(self: Self, user_service: UserServiceProtocol):
        self.user_service = user_service

    async def __call__(self: Self, user_data: RegisterRequestSchema) -> UserReadSchema:
        return await self.user_service.create_user(user_data)