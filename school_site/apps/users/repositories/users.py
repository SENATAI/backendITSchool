import sqlalchemy as sa
from uuid import UUID
from typing import Self, Optional, List
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.core.utils.exceptions import ModelNotFoundException
from school_site.apps.users.models import User
from school_site.apps.users.schemas import UserReadDBSchema, UserCreateSchema, UserUpdateDBSchema, PasswordSchema, UserReadSchema, PaginationResultSchema
from school_site.core.enums import UserRole


class UserRepositoryProtocol(BaseRepositoryImpl[
    User,
    UserReadDBSchema,
    UserCreateSchema,
    UserUpdateDBSchema
]):
    async def get_by_username(self: Self, username: str) -> Optional[UserReadDBSchema]:
        ...

    async def change_password(self: Self, record_id: UUID, password: PasswordSchema) -> UserReadDBSchema:
        ...

    async def get_by_email(self: Self, email: str) -> Optional[UserReadDBSchema]:
       ...

    async def update_password_by_id(self: Self, record_id: UUID, password: PasswordSchema) -> UserReadDBSchema:
        ...
    async def get_all(self: Self, role: Optional[UserRole] = None, limit: int = 10, offset: int = 0 ) -> PaginationResultSchema[UserReadSchema]:
        async with self.session as session:
            count_query = sa.select(sa.func.count(self.model_type.id))
            data_query = sa.select(self.model_type)
        
            if role:
                count_query = count_query.where(self.model_type.role == role)
                data_query = data_query.where(self.model_type.role == role)
        
            total_count = (await session.execute(count_query)).scalar_one()
        
            data_query = data_query.limit(limit).offset(offset)
            models = (await session.execute(data_query)).scalars().all()
            
            # Преобразуем SQLAlchemy модели в Pydantic модели
            pydantic_models = [UserReadSchema.model_validate(model, from_attributes=True) for model in models]
        
            return PaginationResultSchema[UserReadSchema](
                count=total_count,
                objects=pydantic_models
            )

class UserRepository(UserRepositoryProtocol):
    async def get_by_username(self: Self, username: str) -> Optional[UserReadDBSchema]:
        async with self.session as session:
            stmt = sa.select(self.model_type).where(self.model_type.username == username)
            user = (await session.execute(stmt)).scalar_one_or_none()
            if user is None:
               return None
            return self.read_schema_type.model_validate(user, from_attributes=True)
        
    async def change_password(self: Self, record_id: UUID, password: PasswordSchema) -> UserReadDBSchema:
        async with self.session as session, session.begin():
            stmt = (
                sa.update(self.model_type)
                .where(self.model_type.id == record_id)
                .values(password.model_dump())
                .returning(self.model_type)
            )
            user = (await session.execute(stmt)).scalar_one_or_none()
            if user is None:
                raise ModelNotFoundException(self.model_type, record_id)

            return self.read_schema_type.model_validate(user, from_attributes=True)
        
    async def get_by_email(self: Self, email: str) -> Optional[UserReadDBSchema]:
        async with self.session as session:
            stmt = sa.select(self.model_type).where(self.model_type.email == email)
            user = (await session.execute(stmt)).scalar_one_or_none()
            if user is None:
                return None
            return self.read_schema_type.model_validate(user, from_attributes=True)
        
    async def get_all(self: Self, role: Optional[UserRole] = None, limit: int = 10, offset: int = 0 ) -> PaginationResultSchema[UserReadSchema]:
        async with self.session as session:
            count_query = sa.select(sa.func.count(self.model_type.id))
            data_query = sa.select(self.model_type)
        
            if role:
                count_query = count_query.where(self.model_type.role == role)
                data_query = data_query.where(self.model_type.role == role)
        
            total_count = (await session.execute(count_query)).scalar_one()
        
            data_query = data_query.limit(limit).offset(offset)
            models = (await session.execute(data_query)).scalars().all()
            
            pydantic_models = [UserReadSchema.model_validate(model, from_attributes=True) for model in models]
        
            return PaginationResultSchema[UserReadSchema].model_validate({
            "count": total_count,
            "objects": pydantic_models
            })