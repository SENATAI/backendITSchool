import logging
from typing import Protocol
from uuid import UUID
from school_site.core.schemas import PaginationSchema
from ..repositories.lessons import LessonRepositoryProtocol
from ..schemas import (
    LessonCreateSchema,
    LessonCreateDBSchema,
    LessonUpdateDBSchema,
    LessonUpdateSchema,
    LessonReadSchema,
    LessonPaginationResultSchema
)

logger = logging.getLogger(__name__)


class LessonServiceProtocol(Protocol):
    async def create(self, course_id: UUID, lesson: LessonCreateSchema) -> LessonReadSchema:
        ...

    async def get(self, course_id: UUID, lesson_id: UUID) -> LessonReadSchema:
        ...

    async def update(self, course_id: UUID, lesson_id: UUID, lesson: LessonUpdateSchema) -> LessonReadSchema:
        ...

    async def delete(self, course_id: UUID, lesson_id: UUID) -> None:
        ...

    async def list(self, course_id: UUID, pagination: PaginationSchema) -> LessonPaginationResultSchema:
        ...


class LessonService(LessonServiceProtocol):
    def __init__(self, lesson_repository: LessonRepositoryProtocol):
        self.lesson_repository = lesson_repository

    async def create(self, course_id: UUID, lesson: LessonCreateSchema) -> LessonReadSchema:
        db_lesson_create = LessonCreateDBSchema(
            name=lesson.name,
            teacher_material_id=lesson.teacher_material_id,
            student_material_id=lesson.student_material_id,
            homework_id=lesson.homework_id,
            course_id=course_id
        )
        return await self.lesson_repository.create(db_lesson_create)

    async def get(self, course_id: UUID, lesson_id: UUID) -> LessonReadSchema:
        return await self.lesson_repository.get(lesson_id)

    async def update(self, course_id: UUID, lesson_id: UUID, lesson: LessonUpdateSchema) -> LessonReadSchema:
        db_lesson_update = LessonUpdateDBSchema(
            id=lesson_id,
            name=lesson.name,
            teacher_material_id=lesson.teacher_material_id,
            student_material_id=lesson.student_material_id,
            homework_id=lesson.homework_id,
            course_id=course_id
        )
        return await self.lesson_repository.update(db_lesson_update)

    async def delete(self, course_id: UUID, lesson_id: UUID) -> None:
        await self.lesson_repository.delete(lesson_id)

    async def list(self, course_id: UUID, pagination: PaginationSchema) -> LessonPaginationResultSchema:
        return await self.lesson_repository.paginate_by_course(course_id, pagination) 