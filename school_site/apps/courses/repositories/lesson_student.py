from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import LessonStudent
from ..schemas import LessonStudentCreateSchema, LessonStudentUpdateDBSchema, LessonStudentReadSchema


class LessonStudentRepositoryProtocol(BaseRepositoryImpl[
    LessonStudent,
    LessonStudentReadSchema,
    LessonStudentCreateSchema,
    LessonStudentUpdateDBSchema
]):
    pass

class LessonStudentRepository(LessonStudentRepositoryProtocol):
    pass