import sqlalchemy as sa
from uuid import UUID
from typing import Self, Optional
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.core.utils.exceptions import ModelNotFoundException
from school_site.apps.users.models import User
from school_site.apps.users.schemas import UserReadDBSchema, UserCreateSchema, UserUpdateDBSchema, PasswordSchema

class UserRepositoryProtocol(BaseRepositoryImpl[
    User,
    UserReadDBSchema,
    UserCreateSchema,
    UserUpdateDBSchema
]):
    async def get_by_username(self: Self, username: int) -> Optional[UserReadDBSchema]:
        ...

    async def change_password(self: Self, record_id: UUID, password: PasswordSchema) -> UserReadDBSchema:
        ...

    async def get_by_email(self: Self, email: str) -> Optional[UserReadDBSchema]:
       ...

    async def update_password_by_id(self: Self, record_id: UUID, password: PasswordSchema) -> UserReadDBSchema:
        ...

    async def generate_username(self: Self) -> int:
        ...

class UserRepository(UserRepositoryProtocol):
    async def get_by_username(self: Self, username: int) -> Optional[UserReadDBSchema]:
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
        
    async def generate_username(self: Self) -> int:
        async with self.session as session:
            subquery = (
            sa.select(
                self.model_type.username,
                sa.func.row_number().over(order_by=User.username).label("rn")
            )
            .subquery()
        )

            gap_query = (
                sa.select(subquery.c.rn)
                .where(subquery.c.username > subquery.c.rn)
                .order_by(subquery.c.rn)
                .limit(1)
            )

            gap_result = (await session.execute(gap_query)).scalar()

            if gap_result is not None:
                return gap_result

            max_username = (await session.execute(
                sa.select(sa.func.max(self.model_type.username))
            )).scalar() or 0

            return max_username + 1