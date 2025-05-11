from typing import Self, List
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.users.schemas import UserReadSchema
from school_site.apps.users.services.users import UserServiceProtocol

class GetAllUsersUseCaseProtocol(UseCaseProtocol[List[UserReadSchema]]):
    async def __call__(self: Self) -> List[UserReadSchema]:
        ...

class GetAllUsersUseCase(GetAllUsersUseCaseProtocol):
    def __init__(self: Self, user_service: UserServiceProtocol):
        self.user_service = user_service

    async def __call__(self: Self) -> List[UserReadSchema]:
        return await self.user_service.get_all_users()