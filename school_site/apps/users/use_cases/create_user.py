from typing import Self
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.users.schemas import RegisterRequestSchema, UserReadSchema
from school_site.apps.users.services.users import UserServiceProtocol
from school_site.apps.users.services.auth import AuthServiceProtocol
from school_site.core.enums import UserRole
from school_site.core.utils.exceptions import PermissionDeniedError



class CreateUserUseCaseProtocol(UseCaseProtocol[UserReadSchema]):
    async def __call__(self: Self, user_data: RegisterRequestSchema) -> UserReadSchema:
        ...

class CreateUserUseCase(CreateUserUseCaseProtocol):
    def __init__(self: Self, auth_service: AuthServiceProtocol, user_service: UserServiceProtocol):
        self.auth_service = auth_service
        self.user_service = user_service

    async def __call__(self: Self, acess_token: str, user_data: RegisterRequestSchema) -> UserReadSchema:
        current_user = await self.auth_service.get_admin_user(acess_token)
        if current_user.role == UserRole.ADMIN and user_data.role != UserRole.STUDENT:
            raise PermissionDeniedError()
        
        return await self.user_service.create_user(user_data)