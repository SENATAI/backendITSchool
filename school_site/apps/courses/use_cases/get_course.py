from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.courses import CourseServiceProtocol
from ..schemas import CourseReadSchema

class GetCourseUseCaseProtocol(UseCaseProtocol[CourseReadSchema]):
    async def __call__(self, course_id: UUID) -> CourseReadSchema:
        ...

class GetCourseUseCase(GetCourseUseCaseProtocol):
    def __init__(self, course_service: CourseServiceProtocol):
        self.course_service = course_service
    
    async def __call__(self, course_id: UUID) -> CourseReadSchema:
        return await self.course_service.get(course_id)