from uuid import UUID
from school_site.core.schemas import(
    CreateBaseModel, UpdateBaseModel, TimestampMixin, PaginationResultSchema
) 
from school_site.apps.users.schemas import UserReadSchema


class TeacherBaseSchema(TimestampMixin):
    user_id: UUID


class TeacherCreateSchema(CreateBaseModel, TeacherBaseSchema):
    pass


class TeacherUpdateSchema(UpdateBaseModel, TeacherBaseSchema):
    pass


class TeacherReadSchema(TeacherBaseSchema):
    id: UUID


class TeacherReadWithUserSchema(TeacherBaseSchema):
    id: UUID
    user: UserReadSchema


class TeacherPaginationResultSchema(PaginationResultSchema[TeacherReadSchema]):
    pass


class TeacherPaginationWithUserResultSchema(PaginationResultSchema[TeacherReadWithUserSchema]):
    pass 