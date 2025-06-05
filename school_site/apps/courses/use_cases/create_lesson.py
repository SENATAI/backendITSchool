from uuid import UUID
from typing import Protocol
from school_site.core.use_cases import UseCaseProtocol
from ..services.lessons import LessonServiceProtocol
from ..services.auth import AuthAdminServiceProtocol
from ..schemas import LessonCreateSchema, LessonReadSchema


class CreateLessonUseCaseProtocol(UseCaseProtocol):
    async def __call__(self, course_id: UUID, lesson: LessonCreateSchema, access_token: str) -> LessonReadSchema:
        ...


class CreateLessonUseCase(CreateLessonUseCaseProtocol):
    def __init__(
        self,
        lesson_service: LessonServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.lesson_service = lesson_service
        self.auth_service = auth_service

    async def __call__(self, course_id: UUID, lesson: LessonCreateSchema, access_token: str) -> LessonReadSchema:
        await self.auth_service.get_admin_user(access_token)
        return await self.lesson_service.create(course_id, lesson) 