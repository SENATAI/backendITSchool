import logging
from typing import Protocol, List
from ..services.lesson_group import LessonGroupServiceProtocol
from ..services.lesson_student import LessonStudentServiceProtocol
from ..schemas import (
    LessonGroupCreateSchema,
    LessonStudentCreateSchema,
    LessonGroupReadSchema
)
from school_site.apps.students.services.students import StudentsByGroupServiceProtocol  

logger = logging.getLogger(__name__)


class CombinedLessonGroupStudentServiceProtocol(Protocol):
    async def create_lesson_group_with_students(self, lesson_group_data: LessonGroupCreateSchema) -> LessonGroupReadSchema:
        ...

    async def bulk_create_lesson_groups_with_students(self, lesson_groups_data: List[LessonGroupCreateSchema]) -> List[LessonGroupReadSchema]:
        ...


class CombinedLessonGroupStudentService:
    def __init__(
        self,
        lesson_group_service: LessonGroupServiceProtocol,
        lesson_student_service: LessonStudentServiceProtocol,
        student_service: StudentsByGroupServiceProtocol
    ):
        self.lesson_group_service = lesson_group_service
        self.lesson_student_service = lesson_student_service
        self.student_service = student_service

    async def create_lesson_group_with_students(self, lesson_group_data: LessonGroupCreateSchema) -> LessonGroupReadSchema:
        """
        Создает LessonGroup и для каждого студента из группы создает LessonStudent
        """
 
        created_lesson_group = await self.lesson_group_service.create(lesson_group_data)

        students = await self.student_service.get_students_by_group_id(lesson_group_data.group_id)
        if not students:
            logger.warning(f"In group {lesson_group_data.group_id} does not students")
            return created_lesson_group

        lesson_students = [
            LessonStudentCreateSchema(
                student_id=student.id,
                lesson_group_id=created_lesson_group.id
            ) for student in students
        ]

        await self.lesson_student_service.bulk_create(lesson_students)
        logger.info(f"Created {len(lesson_students)} LessonStudent for group {lesson_group_data.group_id}")

        return created_lesson_group

        
    async def bulk_create_lesson_groups_with_students(self, lesson_groups_data: List[LessonGroupCreateSchema]) -> List[LessonGroupReadSchema]:
        """
        Bulk creation of LessonGroups and for each, creation of LessonStudent for students in the group.
        """
        if not lesson_groups_data:
            logger.warning("Received empty list for bulk creation")
            return []

        created_groups = []
        failed_groups = []

        for group_data in lesson_groups_data:
                created_group = await self.create_lesson_group_with_students(group_data)
                created_groups.append(created_group)
            
        if failed_groups:
            logger.warning(f"Failed to create {len(failed_groups)} groups: {failed_groups}")

        return created_groups