from typing import Self
from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.users.schemas import UserReadSchema
from school_site.apps.users.services.users import UserServiceProtocol
from school_site.apps.users.services.auth import AuthServiceProtocol
from school_site.core.utils.exceptions import PermissionDeniedError
from school_site.core.enums import UserRole

class GetUserByIdUseCaseProtocol(UseCaseProtocol[UserReadSchema]):
    async def __call__(self: Self, user_id: UUID) -> UserReadSchema:
        ...

class GetUserByIdUseCase(GetUserByIdUseCaseProtocol):
    def __init__(self: Self, auth_service: AuthServiceProtocol, user_service: UserServiceProtocol):
        self.auth_service = auth_service
        self.user_service = user_service

    async def __call__(self: Self, access_token: str, user_id: UUID) -> UserReadSchema:
        current_user = await self.auth_service.get_admin_user(access_token)
        user = await self.user_service.get_user_by_id(user_id)
        if current_user.role == UserRole.ADMIN and user.role != UserRole.STUDENT:
            raise PermissionDeniedError()
        return user
        
