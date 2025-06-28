from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lesson_student import LessonStudentWithStudentService


class DeleteLessonStudentsAndUpdateStudentsUseCaseProtocol(UseCaseProtocol):
    async def __call__(self, lesson_student_id: UUID) -> bool:
        ...


class DeleteLessonStudentsAndUpdateStudentsUseCase(DeleteLessonStudentsAndUpdateStudentsUseCaseProtocol):
    def __init__(
        self,
        lesson_student_service: LessonStudentWithStudentService,
    ):
        self.lesson_student_service = lesson_student_service

    async def __call__(self, lesson_student_id: UUID) -> bool:
        return await self.lesson_student_service.delete_ls_and_update_student(lesson_student_id)
