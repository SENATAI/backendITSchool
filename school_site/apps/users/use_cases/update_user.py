from typing import Self
from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.users.schemas import UserReadSchema, UserUpdateRequestSchema
from school_site.apps.users.services.users import UserServiceProtocol
from school_site.apps.users.services.auth import AuthServiceProtocol
from school_site.core.enums import UserRole
from school_site.core.utils.exceptions import PermissionDeniedError
from school_site.apps.users.services.permissions import permission_service


class UpdateUserUseCaseProtocol(UseCaseProtocol[UserReadSchema]):
    async def __call__(self: Self, url_user_id: UUID, user_data: UserUpdateRequestSchema) -> UserReadSchema:
        ...

class UpdateUserUseCase(UpdateUserUseCaseProtocol):
    def __init__(self: Self, auth_service: AuthServiceProtocol, user_service: UserServiceProtocol):
        self.auth_service = auth_service
        self.user_service = user_service

    async def __call__(self: Self, access_token: str, url_user_id: UUID, user_data: UserUpdateRequestSchema) -> UserReadSchema:
        current_user = await self.auth_service.get_admin_user(access_token)
        target_user = await self.user_service.update_user_by_router(url_user_id, user_data)

        permission_service.check(
            "update_user",
            current_user=current_user,
            target_user=target_user
        )
        
        if current_user.role == UserRole.ADMIN:
            user_data.role = UserRole.STUDENT
        
        return await self.user_service.update_user_by_router(url_user_id, user_data)