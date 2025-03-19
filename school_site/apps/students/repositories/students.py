import sqlalchemy as sa
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import Student
from ..schemas import StudentCreateSchema, StudentReadSchema, StudentUpdateSchema


class StudentRepositoryProtocol(BaseRepositoryImpl[
    Student,
    StudentReadSchema,
    StudentCreateSchema,
    StudentUpdateSchema
]):
    async def get_by_user_id(self, user_id: UUID) -> StudentReadSchema:
        ...


class StudentRepository(StudentRepositoryProtocol):
    async def get_by_user_id(self, user_id: UUID) -> StudentReadSchema:
        async with self.session as session:
            stmt = sa.select(self.model_type).where(self.model_type.user_id == user_id)
            student = (await session.execute(stmt)).scalar_one_or_none()
            if student is None:
               return None
            return self.read_schema_type.model_validate(student, from_attributes=True)