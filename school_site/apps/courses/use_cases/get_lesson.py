from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.lessons import LessonServiceProtocol
from ..schemas import LessonReadSchema

class GetLessonUseCaseProtocol(UseCaseProtocol[LessonReadSchema]):
    async def __call__(self, course_id: UUID, lesson_id: UUID) -> LessonReadSchema:
        ...

class GetLessonUseCase(GetLessonUseCaseProtocol):
    def __init__(self, lesson_service: LessonServiceProtocol):
        self.lesson_service = lesson_service
    
    async def __call__(self, course_id: UUID, lesson_id: UUID) -> LessonReadSchema:
        return await self.lesson_service.get(course_id, lesson_id) 