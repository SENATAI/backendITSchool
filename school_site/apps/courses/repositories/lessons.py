import sqlalchemy as sa
from sqlalchemy.sql.expression import func
from typing import Self
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.core.schemas import PaginationSchema
from ..models import Lesson
from ..schemas import (
    LessonCreateDBSchema,
    LessonReadDBSchema,
    LessonUpdateDBSchema,
    LessonPaginationResultDBSchema,
    LessonReadDBHeadSchema
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
            statement = sa.select(
                self.model_type.id,
                self.model_type.name,
                self.model_type.course_id
            ).where(self.model_type.course_id == course_id)

            result = await s.execute(statement.limit(pagination.limit).offset(pagination.offset))
            rows = result.all()  
            objects = [
                LessonReadDBHeadSchema.model_validate(
                    {"id": row[0], "name": row[1], "course_id": row[2]}, 
                    from_attributes=True
                )
                for row in rows
            ]

            count_statement = sa.select(sa.func.count(self.model_type.id)).where(
                self.model_type.course_id == course_id
            )
            count = (await s.execute(count_statement)).scalar_one()

            return LessonPaginationResultDBSchema(count=count, objects=objects)

    async def check_teacher_material_exists(self: Self, teacher_material_id: UUID) -> bool:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.teacher_material_id == teacher_material_id)
            result = await s.execute(statement)
            return result.scalar_one_or_none() is not None 