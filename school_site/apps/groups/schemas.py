from pydantic import BaseModel, Field
from uuid import UUID
from school_site.core.schemas import (
    CreateBaseModel, UpdateBaseModel, TimestampMixin, PaginationResultSchema
)

# ====== GROUP SCHEMAS =======

class GroupBaseSchema(BaseModel):
    name: str = Field(..., description="Название группы")
    description: str = Field(..., description="Описание группы")


class GroupCreateSchema(CreateBaseModel, GroupBaseSchema):
    pass


class GroupCreateDBSchema(CreateBaseModel, GroupBaseSchema):
    pass


class GroupUpdateSchema(GroupBaseSchema):
    pass


class GroupUpdateDBSchema(UpdateBaseModel, GroupBaseSchema):
    pass


class GroupReadSchema(GroupBaseSchema, TimestampMixin):
    id: UUID


class GroupReadDBSchema(GroupBaseSchema, TimestampMixin):
    id: UUID


class GroupReadSimpleSchema(BaseModel):
    id: UUID
    name: str


class GroupReadHeadSchema(GroupReadSimpleSchema):
    pass


class GroupReadDBHeadSchema(GroupReadSimpleSchema):
    pass


class GroupPaginationResultSchema(PaginationResultSchema[GroupReadHeadSchema]):
    pass


class GroupDBPaginationResultSchema(PaginationResultSchema[GroupReadDBHeadSchema]):
    pass


# ====== GROUP STUDENTS SCHEMAS =======

class GroupAddStudentsSchema(BaseModel):
    students_id: list[UUID] = Field(..., description="Список ID студентов для добавления в группу")


class GroupAddStudentsDBSchema(GroupAddStudentsSchema):
    pass


# ====== GROUP TEACHER SCHEMAS =======

class GroupAddTeacherSchema(BaseModel):
    teacher_id: UUID = Field(..., description="ID преподавателя для добавления в группу")


class GroupAddTeacherDBSchema(GroupAddTeacherSchema):
    pass
