import logging
from typing import Protocol, Self, List, Optional
from uuid import UUID
from school_site.apps.users.schemas import(
    UserCreateSchema, UserReadSchema, RegisterRequestSchema, UserReadDBSchema,
    UserUpdateSchema, UserUpdateDBSchema, UserUpdateRequestSchema, UserUpdateNoPasswordSchema, UserUpdateDBNoPasswordHashSchema
) 
from school_site.apps.users.repositories.users import UserRepositoryProtocol
from school_site.apps.users.services.passwords import PasswordServiceProtocol
from school_site.apps.users.exceptions import (
    UsernameAlreadyExistsError, InvalidCredentialsError, UsernameNotExistsExceptions
)
from ..schemas import PasswordSchema


logger = logging.getLogger(__name__)


class UserServiceProtocol(Protocol):
    async def create_user(self: Self, user: UserCreateSchema) -> UserReadSchema:
        ...
    
    async def get_user_by_id(self: Self, user_id: UUID) -> UserReadSchema:
        ...
    
    async def _get_user_by_username(self: Self, username: str) -> UserReadDBSchema | None:
        ...
    
    async def authenticate_user(self: Self, username: str, password: str) -> UserReadSchema:
        ...

    async def authenticate_user_by_id(self: Self, user_id: UUID, password: str) -> UserReadSchema:
        ...

    async def update_user(self: Self, user: UserUpdateSchema) -> UserReadSchema:
        ...

    async def change_password(self: Self, record_id: UUID, new_password: str) -> UserReadSchema:
        ...

    async def get_all_users(self: Self) -> List[UserReadSchema]:
        ...

    async def delete_user(self:Self, user_id: UUID) -> bool:
        ...

    async def update_user_by_router(self: Self, url_user_id: UUID, user_data: UserUpdateRequestSchema) -> UserReadSchema:
      ...

    async def get_by_email_or_none(self: Self, email: str) -> Optional[UserReadDBSchema]:
      ...

class UserService(UserServiceProtocol):
    def __init__(
        self: Self,
        user_repository: UserRepositoryProtocol,
        password_service: PasswordServiceProtocol
    ):
        self.user_repository = user_repository
        self.password_service = password_service
    
    async def create_user(self: Self, user: RegisterRequestSchema) -> UserReadSchema:
        logger.info(f"Creating user with username: {user.username}")
        
        existing_user = await self._get_user_by_username(user.username)
        if existing_user:
            logger.error(f"User with username {user.username} already exists")
            raise UsernameAlreadyExistsError()
        
        password_hash = self.password_service.get_password_hash(user.password)
        user_create = UserCreateSchema(
            first_name=user.first_name,
            surname=user.surname,
            patronymic=user.patronymic,
            email=user.email,
            phone_number=user.phone_number,
            username=user.username,
            password_hash=password_hash,
            role=user.role
        )
        new_user = await self.user_repository.create(user_create)
        
        logger.info(f"Successfully created user with id: {new_user.id}")
        return UserReadSchema(**new_user.model_dump(exclude={'password_hash'}))
    
    async def update_user(self: Self, user: UserUpdateSchema) -> UserReadSchema:
        db_user = UserUpdateDBSchema(
            first_name=user.first_name,
            surname=user.surname,
            patronymic=user.patronymic,
            email=user.email,
            phone_number=user.phone_number,
            username=user.username,
            role=user.role
        )
        updated_user = await self.user_repository.update(db_user)
        return UserReadSchema(**updated_user.model_dump(exclude={'password_hash'}))

    async def update_user_by_router(self: Self, url_user_id: UUID, user_data: UserUpdateRequestSchema) -> UserReadSchema:

        update_data = UserUpdateNoPasswordSchema(
            id=url_user_id,
            **user_data.model_dump()
        )
        
        db_user = UserUpdateDBNoPasswordHashSchema(
            id=url_user_id,
            first_name=update_data.first_name,
            surname=update_data.surname,
            patronymic=update_data.patronymic,
            email=update_data.email,
            phone_number=update_data.phone_number,
            username=update_data.username,
            role=update_data.role,
        )
    
        updated_user = await self.user_repository.update(db_user)
        return UserReadSchema(**updated_user.model_dump(exclude={'password_hash'}))

    async def change_password(self: Self, record_id: UUID, new_password: str) -> UserReadSchema:
        password_hash = self.password_service.get_password_hash(new_password)
        password_schema = PasswordSchema(
            password_hash=password_hash
        )
        updated_user =  await self.user_repository.change_password(record_id, password_schema)
        return UserReadSchema(**updated_user.model_dump(exclude={'password_hash'}))

    
    async def get_user_by_id(self: Self, user_id: UUID) -> UserReadSchema:
        logger.info(f"Fetching user with id: {user_id}")
        user = await self._get_user_by_id(user_id)
        return UserReadSchema(**user.model_dump(exclude={'password_hash'}))
    
    async def _get_user_by_id(self: Self, user_id: UUID) -> UserReadDBSchema:
        logger.info(f"Fetching user schema with password with id: {user_id}")
        return await self.user_repository.get(user_id)

    
    async def _get_user_by_username(self: Self, username: str) -> UserReadDBSchema | None:
        user = await self.user_repository.get_by_username(username)
        return user
    
    async def authenticate_user(self: Self, username: str, password: str) -> UserReadSchema:
        logger.info(f"Authenticating user: {username}")
        
        user = await self._get_user_by_username(username)

        if not user:
            raise UsernameNotExistsExceptions(username)
        
        if not self.password_service.verify_password(password, user.password_hash):
            logger.error(f"Authentication failed: Invalid password for user {username}")
            raise InvalidCredentialsError()
        
        logger.info(f"Authentication successful for user: {username}")
        return UserReadSchema(**user.model_dump(exclude={'password_hash'}))
    
    async def authenticate_user_by_id(self: Self, user_id: UUID, password: str) -> UserReadSchema:
        logger.info(f"Authenticating user: {user_id}")
        
        user = await self._get_user_by_id(user_id)

        if not self.password_service.verify_password(password, user.password_hash):
            logger.error(f"Authentication failed: Invalid password for user {user_id}")
            raise InvalidCredentialsError()
        
        logger.info(f"Authentication successful for user: {user_id}")
        return UserReadSchema(**user.model_dump(exclude={'password_hash'}))
    
    async def get_all_users(self: Self) -> List[UserReadSchema]:
        logger.info("Fetching all users")

        users = await self.user_repository.get_all()
        return [UserReadSchema(**user.model_dump(exclude={'password_hash'})) for user in users]
    
    async def delete_user(self: Self, user_id: UUID) -> bool:
        logger.info(f"Deleting user with id: {user_id}")
        
        await self.user_repository.delete(user_id)
        
        logger.info(f"Successfully deleted user with id: {user_id}")
        return True

    async def get_by_email_or_none(self: Self, email: str) -> Optional[UserReadDBSchema]:
        user = await self.user_repository.get_by_email(email)
        if not user:
            return None
        return UserReadSchema(**user.model_dump(exclude={'password_hash'}))
