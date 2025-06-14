import sqlalchemy as sa
from typing import Self, List, Union
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.core.schemas import PaginationSchema
from school_site.apps.students.models import Student
from ..models import Lesson, LessonGroup, LessonStudent
from ..schemas import (
    LessonCreateDBSchema,
    LessonReadDBSchema,
    LessonUpdateDBSchema,
    LessonPaginationResultDBSchema,
    LessonReadDBHeadSchema,
    LessonDetailSchema,
    LessonStudentOpenSchema,
    LessonStudentClosedSchema,
    LessonTeacherDetailSchema
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

    async def get_lesson_for_student(self: Self, lesson_id, student_id) -> LessonDetailSchema:
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
        
    async def get_lesson_for_student(self: Self, lesson_id: UUID, student_id: UUID) -> Union[LessonStudentOpenSchema, LessonStudentClosedSchema]:
        async with self.session as s:
            student_groups = await self._get_student_groups(student_id)

            opened_group = next((group for group in student_groups if group.is_opened), None)

            if opened_group:
                stmt = (
                    sa.select(self.model_type)
                    .where(self.model_type.id == lesson_id)
                    .options(
                        sa.joinedload(self.model_type.student_material),
                        sa.joinedload(self.model_type.homework),
                        sa.joinedload(self.model_type.groups)
                        .where(LessonGroup.id == opened_group.id)
                        .selectinload(LessonGroup.students)
                        .where(LessonStudent.student_id == student_id)
                        .selectinload(LessonStudent.passed_homeworks)
                        .selectinload(LessonStudent.comments)
                        .selectinload(LessonStudent.student)
                        .selectinload(Student.user)
                    )
                )

                result = await s.execute(stmt)
                lesson = result.unique().scalars().first()

                return LessonStudentOpenSchema.model_validate(lesson, from_attributes=True)

            else:
                result = await s.execute(sa.select(self.model_type.name).where(self.model_type.id == lesson_id))
                name = result.scalar()
                return LessonStudentClosedSchema(id=lesson_id, name=name)
            
    async def get_lesson_for_teacher(self: Self, lesson_id: UUID, student_id: UUID) -> LessonTeacherDetailSchema:
        async with self.session as s:
            stmt = (
                sa.select(self.model_type)
                .where(self.model_type.id == lesson_id)
                .options(
                    sa.joinedload(self.model_type.teacher_material),
                    sa.joinedload(self.model_type.homework),
                    sa.joinedload(self.model_type.groups)
                    .selectinload(LessonGroup.students)
                    .where(LessonStudent.student_id == student_id)
                    .selectinload(LessonStudent.passed_homeworks)
                    .selectinload(LessonStudent.comments)
                    .selectinload(LessonStudent.student)
                    .selectinload(Student.user)
                )
            )

            result = await s.execute(stmt)
            lesson = result.unique().scalars().first()

            return LessonTeacherDetailSchema.model_validate(lesson, from_attributes=True)

    async def _get_student_groups(self, student_id: UUID) -> List[LessonGroup]:
        async with self.session as s:
            stmt = (
                sa.select(LessonGroup)
                .join(LessonGroup.students)
                .where(LessonStudent.student_id == student_id)
            )
            result = await s.execute(stmt)
            return result.scalars().all()