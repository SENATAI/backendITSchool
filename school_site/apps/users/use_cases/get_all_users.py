from typing import Self, List, Optional
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.users.schemas import UserReadSchema
from school_site.apps.users.services.users import UserServiceProtocol
from school_site.apps.users.services.auth import AuthServiceProtocol
from school_site.core.enums import UserRole


class GetAllUsersUseCaseProtocol(UseCaseProtocol[List[UserReadSchema]]):
    async def __call__(self: Self) -> List[UserReadSchema]:
        ...

class GetAllUsersUseCase(UseCaseProtocol[List[UserReadSchema]]):
    def __init__(self, auth_service: AuthServiceProtocol, user_service: UserServiceProtocol):
        self.auth_service = auth_service
        self.user_service = user_service

    async def __call__(self: Self, access_token: str, role: Optional[UserRole] = None, limit: int = 10, offset: int = 0) -> List[UserReadSchema]:
        current_user = await self.auth_service.get_admin_user(access_token)
        
        if current_user.role == UserRole.ADMIN:
            role = UserRole.STUDENT
            
        return await self.user_service.get_all_users(role, limit, offset)