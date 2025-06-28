from uuid import UUID
from typing import Self
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lessons import LessonServiceProtocol
from school_site.apps.courses.services.lesson_html_files import LessonHTMLServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import LessonHTMLCreateSchema, LessonHTMLReadSchema, LessonReadSchema


class AddHomeworkToLessonUseCaseProtocol(UseCaseProtocol[LessonReadSchema]):
    async def __call__(self: Self, lesson_id: UUID, homework_material_name: str, homework_material_text: str, access_token: str) -> LessonReadSchema:
        ...

class AddHomeworkToLessonUseCase(AddHomeworkToLessonUseCaseProtocol):
    def __init__(self: Self, lesson_service: LessonServiceProtocol, material_service: LessonHTMLServiceProtocol, auth_service: AuthAdminServiceProtocol):
        self.lesson_service = lesson_service
        self.material_service = material_service
        self.auth_service = auth_service

    async def __call__(self: Self, lesson_id: UUID, homework_material_name: str, homework_material_text: str, access_token: str) -> LessonReadSchema: 
        await self.auth_service.get_admin_user(access_token)

        homework_material = LessonHTMLCreateSchema(
            name=homework_material_name,
            html_text=homework_material_text
        )
        created_material = await self.material_service.create(homework_material)

        return await self.lesson_service.add_homework_to_lesson(lesson_id, created_material.id)