import logging
from typing import Protocol, Self
from uuid import UUID
from ..repositories.lesson_student import LessonStudentRepositoryProtocol
from ..schemas import (
    LessonStudentCreateSchema,
    LessonStudentUpdateSchema,
    LessonStudentReadSchema,
    LessonStudentUpdateDBSchema
)

logger = logging.getLogger(__name__)


class LessonStudentServiceProtocol(Protocol):
    async def create(self: Self, lesson_student: LessonStudentCreateSchema) -> LessonStudentReadSchema:
        ...

    async def get(self: Self, lesson_student_id: UUID) -> LessonStudentReadSchema:
        ...

    async def update(self: Self, lesson_student_id: UUID, LessonStudent: LessonStudentUpdateSchema) -> LessonStudentReadSchema:
        ...

    async def delete(self: Self, lesson_student_id: UUID) -> None:
        ...

    async def bulk_create(self: Self, lesson_students: list[LessonStudentCreateSchema]) -> list[LessonStudentReadSchema]:
        ...


class LessonStudentService(LessonStudentServiceProtocol):
    def __init__(self: Self, lesson_student_repository: LessonStudentRepositoryProtocol):
        self.lesson_student_repository = lesson_student_repository

    async def create(self: Self, lesson_student: LessonStudentCreateSchema) -> LessonStudentReadSchema:
        logger.info("Creating LessonStudent")
        return await self.lesson_student_repository.create(lesson_student)

    async def bulk_create(self: Self, lesson_students: list[LessonStudentCreateSchema]) -> list[LessonStudentReadSchema]:
        logger.info("Bulk creating LessonStudent")
        return await self.lesson_student_repository.bulk_create(lesson_students)

    async def get(self: Self, lesson_student_id: UUID) -> LessonStudentReadSchema:
        logger.info(f"Fetching LessonStudent with ID: {lesson_student_id}")
        return await self.lesson_student_repository.get(lesson_student_id)

    async def update(self: Self, lesson_student_id: UUID, lesson_student: LessonStudentUpdateSchema) -> LessonStudentReadSchema:
        logger.info(f"Updating LessonStudent with ID: {lesson_student_id}")
        db_lesson_student = LessonStudentUpdateDBSchema(
            id=lesson_student_id,
            student_id=lesson_student.student_id,
            lesson_group_id=lesson_student.lesson_group_id,
            is_visited=lesson_student.is_visited,
            is_excused_absence=lesson_student.is_excused_absence,
            is_sent_homework=lesson_student.is_sent_homework,
            is_graded_homework=lesson_student.is_graded_homework,
            coins_for_visit=lesson_student.coins_for_visit,
            coins_for_homework=lesson_student.coins_for_homework
        )
        return await self.lesson_student_repository.update(db_lesson_student)

    async def delete(self: Self, lesson_student_id: UUID) -> None:
        logger.info(f"Deleting LessonStudent with ID: {lesson_student_id}")
        await self.lesson_student_repository.delete(lesson_student_id)


class GetLessonStudentByStudentAndLessonServiceProtocol(Protocol):
        async def get_lesson_student(self: Self, student_id: UUID, lesson_id: UUID) -> LessonStudentReadSchema:
            ...


class GetLessonStudentByStudentAndLessonService(GetLessonStudentByStudentAndLessonServiceProtocol):
    def __init__(self: Self, repository: LessonStudentRepositoryProtocol):
        self.repository = repository
    
    async def get_lesson_student(self: Self, student_id: UUID, lesson_id: UUID) -> LessonStudentReadSchema:
        return await self.repository.get_lesson_student(student_id, lesson_id)