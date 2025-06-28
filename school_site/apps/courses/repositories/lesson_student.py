import sqlalchemy as sa
from typing import Self, Optional, List
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import LessonStudent, LessonGroup
from ..schemas import LessonStudentCreateSchema, LessonStudentUpdateDBSchema, LessonStudentReadSchema, LessonStudentReadWithStudentDBSchema


class LessonStudentRepositoryProtocol(BaseRepositoryImpl[
    LessonStudent,
    LessonStudentReadSchema,
    LessonStudentCreateSchema,
    LessonStudentUpdateDBSchema
    
]):
    async def get_lesson_student(self: Self, student_id: UUID, lesson_id: UUID) -> LessonStudentReadSchema:
        ...
    
    async def get_all_by_lesson_group_id(self: Self, lesson_group_id: UUID, is_graded_homework: Optional[bool] = None) -> List[LessonStudentReadWithStudentDBSchema]:
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
        
    async def get_all_by_lesson_group_id(self, lesson_group_id: UUID, is_graded_homework: Optional[bool] = None) -> List[LessonStudentReadWithStudentDBSchema]:
        async with self.session as s:
            statement = (
                sa.select(LessonStudent)
                .join(LessonStudent.student)
                .where(LessonStudent.lesson_group_id == lesson_group_id)
            )
            
            if is_graded_homework is not None:
                statement = statement.where(LessonStudent.is_graded_homework == is_graded_homework)
            
            result = await s.execute(statement)
            return [LessonStudentReadWithStudentDBSchema.model_validate(model, from_attributes=True) for model in result.scalars().all()]