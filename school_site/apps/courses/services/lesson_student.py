import logging
from typing import Protocol, Self, List, Optional
from uuid import UUID
from ..repositories.lesson_student import LessonStudentRepositoryProtocol
from school_site.core.services.files import FileServiceProtocol
from school_site.apps.students.services.students import StudentServiceProtocol 
from school_site.apps.students.schemas import StudentUpdateSchema
from ..schemas import (
    LessonStudentCreateSchema,
    LessonStudentUpdateSchema,
    LessonStudentReadSchema,
    LessonStudentUpdateDBSchema,
    LessonStudentReadWithStudentSchema,
    LessonStudentDetailReadSchema,
    HomeworkReadSchema,
    FileHomeworkReadSchema,
    LessonStudentWithLessonGroupReadSchema
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

    async def get_all_by_lesson_group_id(self: Self, lesson_group_id: UUID, is_graded_homework: Optional[bool] = None) -> List[LessonStudentReadWithStudentSchema]:
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
            is_compensated_skip=lesson_student.is_compensated_skip,
            is_sent_homework=lesson_student.is_sent_homework,
            is_graded_homework=lesson_student.is_graded_homework,
            coins_for_visit=lesson_student.coins_for_visit,
            coins_for_homework=lesson_student.coins_for_homework
        )
        return await self.lesson_student_repository.update(db_lesson_student)

    async def delete(self: Self, lesson_student_id: UUID) -> None:
        logger.info(f"Deleting LessonStudent with ID: {lesson_student_id}")
        await self.lesson_student_repository.delete(lesson_student_id)

    async def get_all_by_lesson_group_id(self: Self, lesson_group_id: UUID, is_graded_homework: Optional[bool] = None) -> List[LessonStudentReadWithStudentSchema]:
        return await self.lesson_student_repository.get_all_by_lesson_group_id(lesson_group_id, is_graded_homework)


class LessonStudentWithStudentServiceProtocol(Protocol):
    async def create_ls_and_update_student(self: Self, lesson_student: LessonStudentCreateSchema) -> LessonStudentReadSchema:
        ...

    async def update_ls_and_update_student(
        self: Self, lesson_student_id: UUID, lesson_student: LessonStudentUpdateSchema
    ) -> LessonStudentReadSchema:
        ...

    async def delete_ls_and_update_student(self: Self, lesson_student_id: UUID) -> None:
        ...

class LessonStudentWithStudentService(LessonStudentWithStudentServiceProtocol):
    def __init__(self: Self, lesson_student_repository: LessonStudentRepositoryProtocol,
                 student_service: StudentServiceProtocol):
        self.student_service = student_service 
        self.lesson_student_repository = lesson_student_repository

    async def create_ls_and_update_student(self: Self, lesson_student: LessonStudentCreateSchema) -> LessonStudentReadSchema:
        student = await self.student_service.get(lesson_student.student_id)
        lesson_student = await self.lesson_student_repository.create(lesson_student)
        changed_coins = student.points + (lesson_student.coins_for_visit or 0) + (lesson_student.coins_for_homework or 0)
        student_update = StudentUpdateSchema(
            id=lesson_student.student_id,
            user_id=student.user_id,
            points=changed_coins
        )
        await self.student_service.update(lesson_student.student_id, student_update)
        return lesson_student
    async def update_ls_and_update_student(
        self: Self, lesson_student_id: UUID, lesson_student: LessonStudentUpdateSchema
    ) -> LessonStudentReadSchema:
        student = await self.student_service.get(lesson_student.student_id)
        
        old_lesson_student = await self.lesson_student_repository.get(lesson_student_id)

        lesson_student_update_schema = self._build_lesson_student_update_db_schema(
            lesson_student_id=lesson_student_id,
            lesson_student=lesson_student
        )

        updated_lesson_student = await self.lesson_student_repository.update(lesson_student_update_schema)

        changed_coins = student.points - ((old_lesson_student.coins_for_visit or 0) + (old_lesson_student.coins_for_homework or 0)) + \
            ((updated_lesson_student.coins_for_visit or 0) + (updated_lesson_student.coins_for_homework or 0))
        student_update = StudentUpdateSchema(
            id=lesson_student.student_id,
            user_id=student.user_id,
            points=changed_coins
        )
        await self.student_service.update(lesson_student.student_id, student_update)
        return updated_lesson_student
    
    def _build_lesson_student_update_db_schema(
        self: Self, lesson_student_id: UUID, lesson_student: LessonStudentUpdateSchema
    ) -> LessonStudentUpdateDBSchema:
        return LessonStudentUpdateDBSchema(
            id=lesson_student_id,
            student_id=lesson_student.student_id,
            lesson_group_id=lesson_student.lesson_group_id,
            is_visited=lesson_student.is_visited,
            is_excused_absence=lesson_student.is_excused_absence,
            is_sent_homework=lesson_student.is_sent_homework,
            is_compensated_skip=lesson_student.is_compensated_skip,
            is_graded_homework=lesson_student.is_graded_homework,
            coins_for_visit=lesson_student.coins_for_visit,
            coins_for_homework=lesson_student.coins_for_homework
        )

    async def delete_ls_and_update_student(self: Self, lesson_student_id: UUID) -> bool:
        lesson_student = await self.lesson_student_repository.get(lesson_student_id)
        coins_for_visit, coins_for_homework = lesson_student.coins_for_visit or 0, lesson_student.coins_for_homework or 0
        await self.lesson_student_repository.delete(lesson_student_id)
        student = await self.student_service.get(lesson_student.student_id)
        changed_coins = student.points - (coins_for_visit + coins_for_homework)
        student_update = StudentUpdateSchema(
            id=lesson_student.student_id,
            user_id=student.user_id,
            points=changed_coins
        )
        await self.student_service.update(lesson_student.student_id, student_update)
        return True


class GetDetailedLessonStudentByIdServiceProtocol(Protocol):
    async def get_detailed_by_id(self: Self, lesson_student_id: UUID) -> Optional[LessonStudentDetailReadSchema]:
        ...


class GetDetailedLessonStudentByIdService(GetDetailedLessonStudentByIdServiceProtocol):
    def __init__(self: Self, repository: LessonStudentRepositoryProtocol,
                 file_service: FileServiceProtocol):
        self.file_service = file_service
        self.repository = repository
    
    async def get_detailed_by_id(self: Self, lesson_student_id: UUID) -> LessonStudentDetailReadSchema:
        lesson_student =  await self.repository.get_detailed_by_id(lesson_student_id)
        converted_homeworks = []
        for student_homework in lesson_student.passed_homeworks:
            url = None
            if student_homework.file and student_homework.file.path:
                url = await self.file_service.get_url(student_homework.file.path)
            homework_read = HomeworkReadSchema(
                id=student_homework.id,
                file_id=student_homework.file_id,
                homework=FileHomeworkReadSchema(
                    id=student_homework.file.id,
                    name=student_homework.file.name,
                    url=url
                )
            )
            converted_homeworks.append(homework_read)
        
        return LessonStudentDetailReadSchema(
            id=lesson_student.id,
            student_id=lesson_student.student_id,
            lesson_group_id=lesson_student.lesson_group_id,
            is_visited=lesson_student.is_visited,
            is_excused_absence=lesson_student.is_excused_absence,
            is_sent_homework=lesson_student.is_sent_homework,
            is_graded_homework=lesson_student.is_graded_homework,
            is_compensated_skip=lesson_student.is_compensated_skip,
            coins_for_visit=lesson_student.coins_for_visit,
            grade_for_visit=lesson_student.grade_for_visit,
            coins_for_homework=lesson_student.coins_for_homework,
            grade_for_homework=lesson_student.grade_for_homework,
            passed_homeworks=converted_homeworks,
            comments=lesson_student.comments,
        )
    
class GetLessonStudentsByStudentServiceProtocol(Protocol):
    async def get_all_lesson_students_by_student_id(self: Self, student_id: UUID) -> List[LessonStudentReadSchema]:
        ...

class GetLessonStudentsByStudentService(GetLessonStudentsByStudentServiceProtocol):
    def __init__(self: Self, repository: LessonStudentRepositoryProtocol):
        self.repository = repository
    
    async def get_all_lesson_students_by_student_id(self: Self, student_id: UUID) -> List[LessonStudentWithLessonGroupReadSchema]:
        return await self.repository.get_all_lesson_students_by_student_id(student_id)

class GetLessonStudentByStudentAndLessonServiceProtocol(Protocol):
    async def get_lesson_student(self: Self, student_id: UUID, lesson_id: UUID) -> LessonStudentReadSchema:
        ...


class GetLessonStudentByStudentAndLessonService(GetLessonStudentByStudentAndLessonServiceProtocol):
    def __init__(self: Self, repository: LessonStudentRepositoryProtocol):
        self.repository = repository
    
    async def get_lesson_student(self: Self, student_id: UUID, lesson_id: UUID) -> LessonStudentReadSchema:
        return await self.repository.get_lesson_student(student_id, lesson_id)


class GetAllLessonStudentsByLessonGroupServiceProtocol(Protocol):
    async def get_all_lesson_students_by_lesson_group(
        self: Self, lesson_group_id: UUID
    ) -> List[LessonStudentReadWithStudentSchema]:
        ...

class GetAllLessonStudentsByLessonGroupService(GetAllLessonStudentsByLessonGroupServiceProtocol):
    def __init__(self: Self, repository: LessonStudentRepositoryProtocol):
        self.repository = repository
    
    async def get_all_lesson_students_by_lesson_group(
        self: Self, lesson_group_id: UUID
    ) -> List[LessonStudentReadWithStudentSchema]:
        return await self.repository.get_all_lesson_students_by_lesson_group(lesson_group_id)