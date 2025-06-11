from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import LessonGroup
from ..schemas import LessonGroupCreateSchema, LessonGroupUpdateDBSchema, LessonGroupReadSchema


class LessonGroupRepositoryProtocol(BaseRepositoryImpl[
    LessonGroup,
    LessonGroupReadSchema,
    LessonGroupCreateSchema,
    LessonGroupUpdateDBSchema
]):
    pass

class LessonGroupRepository(LessonGroupRepositoryProtocol):
    pass