from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from .enums import AgeCategory
from school_site.core.schemas import (
    CreateBaseModel, UpdateBaseModel, TimestampMixin, PaginationResultSchema
)

# ====== COURSE SCHEMAS =======

class CourseBaseSchema(BaseModel):
    name: str = Field(..., description="Название курса")
    description: str = Field(..., description="Описание курса")
    age_category: AgeCategory = Field(..., description="Возрастная категория курса")
    price: Optional[int] = Field(None, ge=0, description="Цена курса, целое положительное число или null")
    author_name: Optional[str] = Field(None, description="Имя автора курса")


class CourseCreateSchema(CreateBaseModel, CourseBaseSchema):
    pass


class CourseCreateDBSchema(CreateBaseModel, CourseBaseSchema):
    pass


class CourseUpdateSchema(UpdateBaseModel, CourseBaseSchema):
    pass


class CourseUpdateDBSchema(UpdateBaseModel, CourseBaseSchema):
    pass


class CourseReadSchema(CourseBaseSchema, TimestampMixin):
    id: UUID


class CourseReadDBSchema(CourseBaseSchema, TimestampMixin):
    id: UUID


class CourseReadSimpleSchema(BaseModel):
    id: UUID
    name: str


class CourseReadHeadSchema(CourseReadSimpleSchema):
    pass


class CourseReadDBHeadSchema(CourseReadSimpleSchema):
    pass


class CoursePaginationResultSchema(PaginationResultSchema[CourseReadHeadSchema]):
    pass


class CourseDBPaginationResultSchema(PaginationResultSchema[CourseReadDBHeadSchema]):
    pass