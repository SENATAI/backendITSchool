from ..models import LessonHtmlFile
from ..schemas import LessonHTMLCreateDBSchema, LessonHTMLUpdateDBSchema, LessonHTMLReadDBSchema
from school_site.core.repositories.base_repository import BaseRepositoryImpl


class LessonHTMLRepositoryProtocol(BaseRepositoryImpl[
    LessonHtmlFile,
    LessonHTMLReadDBSchema,
    LessonHTMLCreateDBSchema,
    LessonHTMLUpdateDBSchema
]):
    pass

class LessonHTMLRepository(LessonHTMLRepositoryProtocol):
    pass