import sqlalchemy as sa
from sqlalchemy.sql.expression import func
from collections.abc import Iterable
from typing import Self, Any
from uuid import UUID
from school_site.core.utils.exceptions import ModelNotFoundException
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.core.schemas import PaginationSchema
from ..models import Lesson
from ..schemas import (
    LessonCreateDBSchema,
    LessonReadDBSchema,
    LessonUpdateDBSchema,
    LessonPaginationResultDBSchema
)


class LessonRepositoryProtocol(BaseRepositoryImpl[
    Lesson,
    LessonReadDBSchema,
    LessonCreateDBSchema,
    LessonUpdateDBSchema
]):
    async def get_by_course_id(self: Self, course_id: UUID) -> list[LessonReadDBSchema]:
        ...

    async def paginate_by_course(
        self: Self,
        course_id: UUID,
        pagination: PaginationSchema
    ) -> LessonPaginationResultDBSchema:
        ...

    async def check_teacher_material_exists(self: Self, teacher_material_id: UUID) -> bool:
        ...


class LessonRepository(LessonRepositoryProtocol):
    async def get_by_course_id(self: Self, course_id: UUID) -> list[LessonReadDBSchema]:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.course_id == course_id)
            models = (await s.execute(statement)).scalars().all()
            return [LessonReadDBSchema.model_validate(model, from_attributes=True) for model in models]

    async def paginate_by_course(
        self: Self,
        course_id: UUID,
        pagination: PaginationSchema
    ) -> LessonPaginationResultDBSchema:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.course_id == course_id)
            models = (
                (await s.execute(statement.limit(pagination.limit).offset(pagination.offset)))
                .scalars()
                .all()
            )
            objects = [LessonReadDBSchema.model_validate(model, from_attributes=True) for model in models]
            count_statement = statement.with_only_columns(func.count(self.model_type.id))
            count = (await s.execute(count_statement)).scalar_one()
            return LessonPaginationResultDBSchema(count=count, objects=objects)

    async def check_teacher_material_exists(self: Self, teacher_material_id: UUID) -> bool:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.teacher_material_id == teacher_material_id)
            result = await s.execute(statement)
            return result.scalar_one_or_none() is not None 