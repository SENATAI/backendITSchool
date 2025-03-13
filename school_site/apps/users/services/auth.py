import logging
from typing import Protocol
from school_site.apps.users.schemas import AuthReadSchema
from .users import UserServiceProtocol
from .tokens import TokenServiceProtocol

logger = logging.getLogger(__name__)


class AuthServiceProtocol(Protocol):
    async def login(self, username: str, password: str) -> AuthReadSchema:
        ...
    
    async def refresh(self, refresh_token: str) -> AuthReadSchema:
        ...


class AuthService(AuthServiceProtocol):
    def __init__(
        self,
        user_service: UserServiceProtocol,
        token_service: TokenServiceProtocol
    ):
        self.user_service = user_service
        self.token_service = token_service
    
    async def login(self, username: str, password: str) -> AuthReadSchema:
        logger.info(f"Login attempt for user: {username}")
        
        user = await self.user_service.authenticate_user(username, password)
        
        access_token = self.token_service.create_access_token(
            user_id=user.id, 
            role=user.role, 
        )
        
        refresh_data = await self.token_service.create_refresh_token(user.id)
        
        logger.info(f"Login successful for user: {username}")
        
        return AuthReadSchema(user=user,
                              access_token=access_token,
                              refresh_token=refresh_data)
    
    async def refresh(self, refresh_token: str) -> AuthReadSchema:
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