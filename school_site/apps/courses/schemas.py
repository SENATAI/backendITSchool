from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from uuid import UUID
from .enums import AgeCategory
from school_site.core.schemas import (
    CreateBaseModel, UpdateBaseModel, TimestampMixin, PaginationResultSchema
)

# ====== PHOTO SCHEMAS =======

class PhotoBaseSchema(BaseModel):
    name: str = Field(..., description="Название фотографии курса")
    course_id: Optional[UUID] = None

class PhotoCreateSchema(CreateBaseModel, PhotoBaseSchema):
    pass

class PhotoCreateDBSchema(CreateBaseModel, PhotoBaseSchema):
    course_id: UUID
    path: str

class PhotoUpdateSchema(PhotoBaseSchema):
    id: Optional[UUID] = None

class PhotoUpdateDBSchema(UpdateBaseModel, PhotoBaseSchema):
    course_id: UUID

class PhotoReadDBSchema(PhotoBaseSchema, TimestampMixin):
    id: UUID
    path: str

    class Config:
        from_attributes = True

class PhotoReadSchema(PhotoBaseSchema, TimestampMixin):
    id: UUID
    url: HttpUrl

# --------------------------------
# ====== COURSE SCHEMAS =======

class CourseBaseSchema(BaseModel):
    name: str = Field(..., description="Название курса")
    description: str = Field(..., description="Описание курса")
    age_category: AgeCategory = Field(..., description="Возрастная категория курса")
    price: Optional[int] = Field(None, ge=0, description="Цена курса, целое положительное число или null")
    author_name: Optional[str] = Field(None, description="Имя автора курса")


class CourseCreateSchema(CreateBaseModel, CourseBaseSchema):
    photo: Optional[PhotoCreateSchema] = Field(None, description="Фотография курса (опционально)")


class CourseCreateDBSchema(CreateBaseModel, CourseBaseSchema):
    pass


class CourseUpdateSchema(CourseBaseSchema):
    photo: Optional[PhotoUpdateSchema] = None


class CourseUpdateDBSchema(UpdateBaseModel, CourseBaseSchema):
    pass


class CourseReadSchema(CourseBaseSchema, TimestampMixin):
    id: UUID


class CourseReadDBSchema(CourseBaseSchema, TimestampMixin):
    id: UUID


class CourseWithPhotoReadDBSchema(CourseBaseSchema, TimestampMixin):
    id: UUID
    photo: Optional[PhotoReadDBSchema] = None


class CourseWithPhotoReadSchema(CourseBaseSchema, TimestampMixin):
    id: UUID
    photo: Optional[PhotoReadSchema] = None


class CourseWithPhotoPaginationResultDBSchema(PaginationResultSchema[CourseWithPhotoReadDBSchema]):
    pass


class CourseWithPhotoPaginationResultSchema(PaginationResultSchema[CourseWithPhotoReadSchema]):
    pass


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

# ====== LESSON SCHEMAS =======

class LessonBaseSchema(BaseModel):
    teacher_material_id: UUID = Field(..., description="ID материала для учителя")
    student_material_id: UUID = Field(..., description="ID материала для студента")
    homework_id: UUID = Field(..., description="ID домашнего задания")


class LessonCreateSchema(CreateBaseModel, LessonBaseSchema):
    pass


class LessonCreateDBSchema(CreateBaseModel, LessonBaseSchema):
    pass


class LessonUpdateSchema(LessonBaseSchema):
    pass


class LessonUpdateDBSchema(UpdateBaseModel, LessonBaseSchema):
    pass


class LessonReadSchema(LessonBaseSchema, TimestampMixin):
    id: UUID
    course_id: UUID


class LessonReadDBSchema(LessonReadSchema):
    pass


class LessonReadSimpleSchema(BaseModel):
    id: UUID
    teacher_material_id: UUID


class LessonReadHeadSchema(LessonReadSimpleSchema):
    pass


class LessonReadDBHeadSchema(LessonReadSimpleSchema):
    pass


class LessonPaginationResultSchema(PaginationResultSchema[LessonReadHeadSchema]):
    pass


class LessonPaginationResultDBSchema(PaginationResultSchema[LessonReadDBHeadSchema]):
    pass