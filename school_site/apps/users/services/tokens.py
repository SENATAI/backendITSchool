import logging
import hashlib
import secrets
from jose import JWTError, jwt
from typing import Protocol, Optional
from uuid import UUID
from datetime import datetime, timedelta, timezone
from school_site.core.enums import UserRole
from school_site.apps.users.schemas import (
    UserTokenDataReadSchema, TokenReadSchema, RefreshTokenCreateDBSchema, RefreshTokenReadDBSchema
)
from school_site.apps.users.exceptions import InvalidTokenError
from school_site.apps.users.repositories.refresh_tokens import RefreshTokenRepositoryProtocol
from school_site.settings import settings


logger = logging.getLogger(__name__)


class TokenServiceProtocol(Protocol):
    def create_access_token(self, user_id: UUID, role: UserRole, expires_delta: Optional[timedelta] = None) -> TokenReadSchema:
        ...
    
    async def create_refresh_token(self, user_id: UUID) -> TokenReadSchema:
        ...
    
    async def verify_refresh_token(self, refresh_token: str) -> RefreshTokenReadDBSchema:
        ...
    
    def decode_access_token(self, token: str) -> UserTokenDataReadSchema:
        ...

    async def delete(self, id: UUID) -> bool:
        ...


class TokenService(TokenServiceProtocol):
    def __init__(
        self,
        refresh_token_repository: RefreshTokenRepositoryProtocol,
    ):
        self.refresh_token_repository = refresh_token_repository
    

    async def delete(self, id: UUID) -> bool:
        return await self.refresh_token_repository.delete(id)
    

    def create_access_token(
        self, 
        user_id: UUID, 
        role: UserRole, 
        expires_delta: Optional[timedelta] = None
    ) -> TokenReadSchema:
        logger.info(f"Creating access token for user: {user_id}")
        
        to_encode = {"user_id": str(user_id), "role": role}
        expiration = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token.token_lifetime_minutes))
        to_encode.update({"exp": expiration})
        
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt.token_algorithm)
        logger.info(f"Access token created for user: {user_id}")
        
        return TokenReadSchema(token=encoded_jwt,
                               expiration=expiration)
    
    async def create_refresh_token(self, user_id: UUID) -> TokenReadSchema:
        logger.info(f"Creating refresh token for user: {user_id}")
        
        refresh_token = secrets.token_hex(32)

        expiration = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token.token_lifetime_days)
        
        hashed_refresh_token = hashlib.sha256(refresh_token.encode('utf-8')).hexdigest()
                
        token_count = await self.refresh_token_repository.count_by_user_id(user_id)
        logger.info(f"User {user_id} has {token_count} refresh tokens")
        
        if token_count >= 5:
            logger.info(f"User {user_id} has reached maximum refresh tokens, removing oldest")
            oldest_token = await self.refresh_token_repository.get_oldest_by_user_id(user_id)
            if oldest_token:
                await self.delete(oldest_token.id)
        
        await self.refresh_token_repository.create(RefreshTokenCreateDBSchema(
            user_id=user_id,
            hashed_refresh_token=hashed_refresh_token
        ))
        logger.info(f"Refresh token created for user: {user_id}")
        
        return TokenReadSchema(
            token=refresh_token,
            expiration=expiration
        )


    async def verify_refresh_token(self, refresh_token: str) -> RefreshTokenReadDBSchema:
        logger.info("Verifying refresh token")
        
        computed_hash = hashlib.sha256(refresh_token.encode('utf-8')).hexdigest()
        
        db_refresh_token = await self.refresh_token_repository.get_by_hashed_token(computed_hash)
        
        if not db_refresh_token:
            logger.error("No matching refresh token found")
            raise InvalidTokenError()
        
        expiration = db_refresh_token.created_at + timedelta(days=settings.refresh_token.token_lifetime_days)
        
        if datetime.now(timezone.utc) > expiration:
            logger.warning(f"Refresh token expired for user: {db_refresh_token.user_id}")
            await self.delete(db_refresh_token.id)
            raise InvalidTokenError()

        return db_refresh_token

    
    def decode_access_token(self, token: str) -> UserTokenDataReadSchema:
        logger.info("Decoding access token")
        
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt.token_algorithm])
            user_id_str = payload.get("user_id")
            role = payload.get("role")
            exp = payload.get("exp")
            
            if user_id_str is None:
                logger.error("Invalid token: missing user_id")
                raise InvalidTokenError()
            
            try:
                user_id = UUID(user_id_str)
            except ValueError:
                logger.error("Invalid token: user_id not a valid UUID")
                raise InvalidTokenError()
            
            token_data = UserTokenDataReadSchema(user_id=user_id, role=UserRole(role), expiration=datetime.fromtimestamp(exp))
            logger.info(f"Token decoded successfully for user: {user_id}")
            
            return token_data
        
        except JWTError:
            logger.warning("Failed to decode token")
            raise InvalidTokenError()
        
    