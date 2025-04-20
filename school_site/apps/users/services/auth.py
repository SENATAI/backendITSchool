import logging
from typing import Protocol, Self
from uuid import UUID
from school_site.core.enums import UserRole
from ..schemas import AuthReadSchema, PasswordChangeSchema, UserUpdateSchema
from .users import UserServiceProtocol
from .tokens import TokenServiceProtocol

logger = logging.getLogger(__name__)


class AuthServiceProtocol(Protocol):
    async def login(self: Self, username: str, password: str) -> AuthReadSchema:
        ...
    
    async def refresh(self: Self, refresh_token: str) -> AuthReadSchema:
        ...

    async def logout(self: Self, refresh_token: str) -> None:
        ...

    async def change_password(self: Self, access_token: str, password: PasswordChangeSchema) -> AuthReadSchema:
        ...

class AuthService(AuthServiceProtocol):
    def __init__(
        self: Self,
        user_service: UserServiceProtocol,
        token_service: TokenServiceProtocol
    ):
        self.user_service = user_service
        self.token_service = token_service
    
    async def change_password(self: Self, access_token: str, password: PasswordChangeSchema) -> AuthReadSchema:
        user_data = await self.token_service.decode_access_token(access_token)
        user = await self.user_service.authenticate_user_by_id(user_data.user_id, password.old_password)
        user_for_update = UserUpdateSchema(
            id=user.id,
            username=user.username,
            password=password.new_password,
            role=user.role
        )
        updated_user = await self.user_service.update_user(user_for_update)
        new_access_token, new_refresh_data = await self._create_tokens(updated_user.id, updated_user.role)

        return AuthReadSchema(user=updated_user,
                              access_token=new_access_token,
                              refresh_token=new_refresh_data)
    
    async def login(self: Self, username: str, password: str) -> AuthReadSchema:
        logger.info(f"Login attempt for user: {username}")
        
        user = await self.user_service.authenticate_user(username, password)
        
        access_token, refresh_data = await self._create_tokens(user.id, user.role)
        
        logger.info(f"Login successful for user: {username}")
        
        return AuthReadSchema(user=user,
                              access_token=access_token,
                              refresh_token=refresh_data)
    
    async def _create_tokens(self: Self, user_id: UUID, role: UserRole) -> tuple[str, str]:
        access_token = self.token_service.create_access_token(
            user_id=user_id, 
            role=role, 
        )
        
        refresh_data = await self.token_service.create_refresh_token(user_id)

        return access_token, refresh_data
    
    async def refresh(self: Self, refresh_token: str) -> AuthReadSchema:
        logger.info("Refreshing tokens")
        
        db_token = await self.token_service.verify_refresh_token(refresh_token)
        
        user = await self.user_service.get_user_by_id(db_token.user_id)
        
        await self.token_service.delete(db_token.id)
        
        access_token = self.token_service.create_access_token(
            user_id=user.id, 
            role=user.role, 
        )
        
        new_refresh_data = await self.token_service.create_refresh_token(user.id)
        
        logger.info(f"Tokens refreshed successfully for user: {user.id}")
        
        return AuthReadSchema(user=user,
                              access_token=access_token,
                              refresh_token=new_refresh_data)
    
    
    async def logout(self: Self, refresh_token: str) -> None:
        db_token = await self.token_service.verify_refresh_token(refresh_token)
        user_id = db_token.user_id
        logger.info(f"Logout for user: {user_id}")
        if db_token:
            await self.token_service.delete(db_token.id)
            logger.info(f"Refresh token removed for user: {user_id}")
        
        logger.info(f"Logout successful for user: {user_id}")