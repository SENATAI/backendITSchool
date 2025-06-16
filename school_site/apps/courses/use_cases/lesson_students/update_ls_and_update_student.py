from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lesson_student import LessonStudentWithStudentService
from school_site.apps.courses.schemas import LessonStudentReadSchema, LessonStudentUpdateSchema


class UpdateLessonStudentsAndUpdateStudentsUseCaseProtocol(UseCaseProtocol):
    async def __call__(self, lesson_student_id: UUID, lesson_student: LessonStudentUpdateSchema) -> LessonStudentReadSchema:
        ...


class UpdateLessonStudentsAndUpdateStudentsUseCase(UpdateLessonStudentsAndUpdateStudentsUseCaseProtocol):
    def __init__(
        self,
        lesson_student_service: LessonStudentWithStudentService,
    ):
        self.lesson_student_service = lesson_student_service

    async def __call__(self, lesson_student_id: UUID, lesson_student: LessonStudentUpdateSchema) -> LessonStudentReadSchema:
        return await self.lesson_student_service.update_ls_and_update_student(lesson_student_id, lesson_student)
