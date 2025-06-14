import sqlalchemy as sa
from typing import Self
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import LessonStudent, LessonGroup
from ..schemas import LessonStudentCreateSchema, LessonStudentUpdateDBSchema, LessonStudentReadSchema


class LessonStudentRepositoryProtocol(BaseRepositoryImpl[
    LessonStudent,
    LessonStudentReadSchema,
    LessonStudentCreateSchema,
    LessonStudentUpdateDBSchema
]):
    async def get_lesson_student(self: Self, student_id: UUID, lesson_id: UUID) -> LessonStudentReadSchema:
        ...


class LessonStudentRepository(LessonStudentRepositoryProtocol):
    async def get_lesson_student(self: Self, student_id: UUID, lesson_id: UUID) -> LessonStudentReadSchema:
        async with self.session as s:
            stmt = (
                sa.select(self.model_type)
                .join(LessonGroup)
                .where(
                    self.model_type.student_id == student_id,
                    LessonGroup.lesson_id == lesson_id
                )
            )
            
            model = (await s.execute(stmt)).scalar_one()
            return LessonStudentReadSchema.model_validate(model, from_attributes=True)