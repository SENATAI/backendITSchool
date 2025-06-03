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


class GroupStudentsBaseSchema(BaseModel):
    students_id: list[UUID] = Field(..., description="Список ID студентов для добавления в группу")


class GroupAddStudentsSchema(GroupStudentsBaseSchema):
    pass


class GroupAddStudentsDBSchema(GroupStudentsBaseSchema):
    pass


class GroupReadStudentsSchema(GroupReadSchema, GroupStudentsBaseSchema):
    pass


class GroupReadStudentsDBSchema(GroupReadDBSchema, GroupStudentsBaseSchema):
    pass


class GroupUpdateStudentsSchema(GroupStudentsBaseSchema):
    pass


class GroupUpdateStudentsDBSchema(GroupStudentsBaseSchema):
    pass


# ====== GROUP TEACHER SCHEMAS =======


class GroupTeacherBaseSchema(BaseModel):
    teacher_id: UUID = Field(..., description="ID преподавателя для добавления в группу")


class GroupAddTeacherSchema(GroupTeacherBaseSchema):
    pass


class GroupAddTeacherDBSchema(GroupTeacherBaseSchema):
    pass


class GroupReadTeacherSchema(GroupReadSchema, GroupTeacherBaseSchema):
    pass


class GroupReadTeacherDBSchema(GroupReadDBSchema, GroupTeacherBaseSchema):
    pass


class GroupUpdateTeacherSchema(GroupTeacherBaseSchema):
    pass


class GroupUpdateTeacherDBSchema(GroupTeacherBaseSchema):
    pass



