import logging
from typing import Protocol
from uuid import UUID
from school_site.apps.users.schemas import(
    UserCreateSchema, UserReadSchema, RegisterRequestSchema, UserReadDBSchema
) 
from school_site.apps.users.repositories.users import UserRepositoryProtocol
from school_site.apps.users.services.passwords import PasswordServiceProtocol
from school_site.apps.users.exceptions import (
    UsernameAlreadyExistsError, InvalidCredentialsError, UsernameNotExistsExceptions
)
from school_site.core.enums import UserRole


logger = logging.getLogger(__name__)


class UserServiceProtocol(Protocol):
    async def create_user(self, user: UserCreateSchema) -> UserReadSchema:
        ...
    
    async def get_user_by_id(self, user_id: UUID) -> UserReadSchema:
        ...
    
    async def _get_user_by_username(self, username: str) -> UserReadDBSchema | None:
        ...
    
    async def authenticate_user(self, username: str, password: str) -> UserReadSchema:
        ...


class UserService(UserServiceProtocol):
    def __init__(
        self,
        user_repository: UserRepositoryProtocol,
        password_service: PasswordServiceProtocol
    ):
        self.user_repository = user_repository
        self.password_service = password_service
    
    async def create_user(self, user: RegisterRequestSchema) -> UserReadSchema:
        logger.info(f"Creating user with username: {user.username}")
        
        existing_user = await self._get_user_by_username(user.username)
        if existing_user:
            logger.error(f"User with username {user.username} already exists")
            raise UsernameAlreadyExistsError()
        
        password = self.password_service.get_password_hash(user.password)
        user_create = UserCreateSchema(
            username=user.username,
            password_hash=password,
            role=UserRole(user.role)
        )
        new_user = await self.user_repository.create(user_create)
        
        logger.info(f"Successfully created user with id: {new_user.id}")
        return UserReadSchema(**new_user.model_dump(exclude={'password_hash'}))
    
    async def get_user_by_id(self, user_id: UUID) -> UserReadSchema:
        logger.info(f"Fetching user with id: {user_id}")
        user = await self.user_repository.get(user_id)
        return UserReadSchema(**user.model_dump(exclude={'password_hash'}))

    
    async def _get_user_by_username(self, username: str) -> UserReadDBSchema | None:
        user = await self.user_repository.get_by_username(username)
        return user
    
    async def authenticate_user(self, username: str, password: str) -> UserReadSchema:
        logger.info(f"Authenticating user: {username}")
        
        user = await self._get_user_by_username(username)

        if not user:
            raise UsernameNotExistsExceptions(username)
        
        if not self.password_service.verify_password(password, user.password_hash):
            logger.error(f"Authentication failed: Invalid password for user {username}")
            raise InvalidCredentialsError()
        
        logger.info(f"Authentication successful for user: {username}")
        return UserReadSchema(**user.model_dump(exclude={'password_hash'}))