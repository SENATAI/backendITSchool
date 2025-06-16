from typing import List, Protocol
from uuid import UUID
from datetime import datetime
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.apps.courses.models import LessonGroup, Lesson, Course
from school_site.apps.students.models import Student
from school_site.apps.teachers.models import Teacher
from school_site.apps.groups.models import GroupStudent, Group
from school_site.apps.users.services.auth import AuthServiceProtocol
from ..schemas import ScheduleReadSchema

class ScheduleRepositoryProtocol(BaseRepositoryImpl[LessonGroup, ScheduleReadSchema, None, None]):
    async def get_student_schedule(self, user_id: UUID) -> List[ScheduleReadSchema]:
        ...
    
    async def get_teacher_schedule(self, user_id: UUID) -> List[ScheduleReadSchema]:
        ...

    async def get_filtered_student_schedule(
        self,
        user_id: UUID,
        date_start: datetime,
        date_end: datetime
    ) -> List[ScheduleReadSchema]:
        ...

    async def get_filtered_teacher_schedule(
        self,
        user_id: UUID,
        date_start: datetime,
        date_end: datetime
    ) -> List[ScheduleReadSchema]:
        ...

    async def get_all_groups_schedule(self) -> List[ScheduleReadSchema]:
        ...

    async def get_filtered_all_groups_schedule(
        self,
        date_start: datetime,
        date_end: datetime
    ) -> List[ScheduleReadSchema]:
        ...

class ScheduleRepository(ScheduleRepositoryProtocol):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_student_schedule(self, user_id: UUID) -> List[ScheduleReadSchema]:
        async with self.session as session:
            student_stmt = select(Student.id).where(Student.user_id == user_id)
            student_result = await session.execute(student_stmt)
            student_id = student_result.scalar_one_or_none()
            
            if not student_id:
                return []

            stmt = (
                select(LessonGroup)
                .options(
                    selectinload(LessonGroup.lesson).selectinload(Lesson.course)
                )
                .join(GroupStudent, GroupStudent.group_id == LessonGroup.group_id)
                .where(GroupStudent.student_id == student_id)
                .order_by(LessonGroup.start_datetime)
            )
            result = await session.execute(stmt)
            lesson_groups = result.scalars().all()
            
            return [
                ScheduleReadSchema(
                    id=group.id,
                    lesson_id=group.lesson_id,
                    group_id=group.group_id,
                    start_datetime=group.start_datetime,
                    end_datetime=group.end_datetime,
                    auditorium=group.auditorium,
                    is_opened=group.is_opened,
                    lesson_name=group.lesson.name,
                    course_name=group.lesson.course.name
                )
                for group in lesson_groups
            ]

    async def get_teacher_schedule(self, user_id: UUID) -> List[ScheduleReadSchema]:
        async with self.session as session:
            teacher_stmt = select(Teacher.id).where(Teacher.user_id == user_id)
            teacher_result = await session.execute(teacher_stmt)
            teacher_id = teacher_result.scalar_one_or_none()
            
            if not teacher_id:
                return []

            stmt = (
                select(LessonGroup)
                .options(
                    selectinload(LessonGroup.lesson).selectinload(Lesson.course)
                )
                .join(Group, Group.id == LessonGroup.group_id)
                .where(Group.teacher_id == teacher_id)
                .order_by(LessonGroup.start_datetime)
            )
            result = await session.execute(stmt)
            lesson_groups = result.scalars().all()
            
            return [
                ScheduleReadSchema(
                    id=group.id,
                    lesson_id=group.lesson_id,
                    group_id=group.group_id,
                    start_datetime=group.start_datetime,
                    end_datetime=group.end_datetime,
                    auditorium=group.auditorium,
                    is_opened=group.is_opened,
                    lesson_name=group.lesson.name,
                    course_name=group.lesson.course.name
                )
                for group in lesson_groups
            ]

    async def get_filtered_student_schedule(
        self,
        user_id: UUID,
        date_start: datetime,
        date_end: datetime
    ) -> List[ScheduleReadSchema]:
        async with self.session as session:
            student_stmt = select(Student.id).where(Student.user_id == user_id)
            student_result = await session.execute(student_stmt)
            student_id = student_result.scalar_one_or_none()
            
            if not student_id:
                return []

            stmt = (
                select(LessonGroup)
                .options(
                    selectinload(LessonGroup.lesson).selectinload(Lesson.course)
                )
                .join(GroupStudent, GroupStudent.group_id == LessonGroup.group_id)
                .where(
                    and_(
                        GroupStudent.student_id == student_id,
                        LessonGroup.start_datetime >= date_start,
                        LessonGroup.end_datetime <= date_end
                    )
                )
                .order_by(LessonGroup.start_datetime)
            )
            result = await session.execute(stmt)
            lesson_groups = result.scalars().all()
            
            return [
                ScheduleReadSchema(
                    id=group.id,
                    lesson_id=group.lesson_id,
                    group_id=group.group_id,
                    start_datetime=group.start_datetime,
                    end_datetime=group.end_datetime,
                    auditorium=group.auditorium,
                    is_opened=group.is_opened,
                    lesson_name=group.lesson.name,
                    course_name=group.lesson.course.name
                )
                for group in lesson_groups
            ]

    async def get_filtered_teacher_schedule(
        self,
        user_id: UUID,
        date_start: datetime,
        date_end: datetime
    ) -> List[ScheduleReadSchema]:
        async with self.session as session:
            teacher_stmt = select(Teacher.id).where(Teacher.user_id == user_id)
            teacher_result = await session.execute(teacher_stmt)
            teacher_id = teacher_result.scalar_one_or_none()
            
            if not teacher_id:
                return []

            stmt = (
                select(LessonGroup)
                .options(
                    selectinload(LessonGroup.lesson).selectinload(Lesson.course)
                )
                .join(Group, Group.id == LessonGroup.group_id)
                .where(
                    and_(
                        Group.teacher_id == teacher_id,
                        LessonGroup.start_datetime >= date_start,
                        LessonGroup.end_datetime <= date_end
                    )
                )
                .order_by(LessonGroup.start_datetime)
            )
            result = await session.execute(stmt)
            lesson_groups = result.scalars().all()
            
            return [
                ScheduleReadSchema(
                    id=group.id,
                    lesson_id=group.lesson_id,
                    group_id=group.group_id,
                    start_datetime=group.start_datetime,
                    end_datetime=group.end_datetime,
                    auditorium=group.auditorium,
                    is_opened=group.is_opened,
                    lesson_name=group.lesson.name,
                    course_name=group.lesson.course.name
                )
                for group in lesson_groups
            ]

    async def get_all_groups_schedule(self) -> List[ScheduleReadSchema]:
        async with self.session as session:
            stmt = (
                select(LessonGroup)
                .options(
                    selectinload(LessonGroup.lesson).selectinload(Lesson.course)
                )
                .order_by(LessonGroup.start_datetime)
            )
            result = await session.execute(stmt)
            lesson_groups = result.scalars().all()
            
            return [
                ScheduleReadSchema(
                    id=group.id,
                    lesson_id=group.lesson_id,
                    group_id=group.group_id,
                    start_datetime=group.start_datetime,
                    end_datetime=group.end_datetime,
                    auditorium=group.auditorium,
                    is_opened=group.is_opened,
                    lesson_name=group.lesson.name,
                    course_name=group.lesson.course.name
                )
                for group in lesson_groups
            ]

    async def get_filtered_all_groups_schedule(
        self,
        date_start: datetime,
        date_end: datetime
    ) -> List[ScheduleReadSchema]:
        async with self.session as session:
            stmt = (
                select(LessonGroup)
                .options(
                    selectinload(LessonGroup.lesson).selectinload(Lesson.course)
                )
                .where(
                    and_(
                        LessonGroup.start_datetime >= date_start,
                        LessonGroup.end_datetime <= date_end
                    )
                )
                .order_by(LessonGroup.start_datetime)
            )
            result = await session.execute(stmt)
            lesson_groups = result.scalars().all()
            
            return [
                ScheduleReadSchema(
                    id=group.id,
                    lesson_id=group.lesson_id,
                    group_id=group.group_id,
                    start_datetime=group.start_datetime,
                    end_datetime=group.end_datetime,
                    auditorium=group.auditorium,
                    is_opened=group.is_opened,
                    lesson_name=group.lesson.name,
                    course_name=group.lesson.course.name
                )
                for group in lesson_groups
            ] 