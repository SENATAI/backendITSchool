from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.courses import CourseServiceProtocol

class DeleteCourseUseCaseProtocol(UseCaseProtocol[None]):
    async def __call__(self, course_id: UUID) -> None:
        ...

class DeleteCourseUseCase(DeleteCourseUseCaseProtocol):
    def __init__(self, course_service: CourseServiceProtocol):
        self.course_service = course_service
    
    async def __call__(self, course_id: UUID) -> None:
        return await self.course_service.delete(course_id)