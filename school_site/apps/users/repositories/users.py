import sqlalchemy as sa
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.apps.users.models import User
from school_site.apps.users.schemas import UserReadDBSchema, UserCreateSchema, UserUpdateDBSchema

class UserRepositoryProtocol(BaseRepositoryImpl[
    User,
    UserReadDBSchema,
    UserCreateSchema,
    UserUpdateDBSchema
]):
    async def get_by_username(username: str) -> UserReadDBSchema | None:
        ...


class UserRepository(UserRepositoryProtocol):
    async def get_by_username(self, username: str) -> UserReadDBSchema | None:
        async with self.session as session:
            stmt = sa.select(self.model_type).where(self.model_type.username == username)
            user = (await session.execute(stmt)).scalar_one_or_none()
            if user is None:
               return None
            return self.read_schema_type.model_validate(user, from_attributes=True)