from typing import Self
from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.core.enums import UserRole
from school_site.core.utils.exceptions import PermissionDeniedError
from school_site.apps.courses.services.lesson_html_files import LessonHTMLServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import LessonHTMLTextUpdateSchema, LessonHTMLReadSchema

class UpdateLessonHTMLFileByTextUseCaseProtocol(UseCaseProtocol[LessonHTMLReadSchema]):
    async def __call__(self: Self, file_id: UUID, lesson: LessonHTMLTextUpdateSchema, access_token: str) -> LessonHTMLReadSchema:
        ...

class UpdateLessonHTMLFileByTextUseCase(UpdateLessonHTMLFileByTextUseCaseProtocol):
    def __init__(self, lesson_service: LessonHTMLServiceProtocol, auth_service: AuthAdminServiceProtocol):
        self.lesson_service = lesson_service
        self.auth_service = auth_service
    
    async def __call__(self: Self, file_id: UUID, lesson: LessonHTMLTextUpdateSchema, access_token: str) -> LessonHTMLReadSchema:
        user_data = await self.auth_service.decode_access_token(access_token)
        if user_data.role not in [UserRole.TEACHER, UserRole.ADMIN, UserRole.SUPERADMIN]:
            raise PermissionDeniedError()
        return await self.lesson_service.update_by_text(file_id, lesson)