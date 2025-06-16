import sqlalchemy as sa
from sqlalchemy.orm import joinedload
from typing import List
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import LessonGroup
from ..schemas import LessonGroupCreateSchema, LessonGroupUpdateDBSchema, LessonGroupReadSchema, \
    LessonGroupReadWithLessonSchema

class LessonGroupRepositoryProtocol(BaseRepositoryImpl[
    LessonGroup,
    LessonGroupReadSchema,
    LessonGroupCreateSchema,
    LessonGroupUpdateDBSchema
]):
    async def get_by_group_id(self, group_id: UUID) -> List[LessonGroupReadWithLessonSchema]:
        ...

class LessonGroupRepository(LessonGroupRepositoryProtocol):
    async def get_by_group_id(self, group_id: UUID) -> List[LessonGroupReadWithLessonSchema]:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.group_id == group_id).options(
                joinedload(self.model_type.lesson)
            )
            result = await s.execute(statement)
            lesson_groups = result.scalars().all()
            return [
                LessonGroupReadWithLessonSchema.model_validate(lesson_group, from_attributes=True) 
                for lesson_group in lesson_groups
            ]
    
