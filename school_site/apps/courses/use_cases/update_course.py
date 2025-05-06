from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.courses import CourseServiceProtocol
from ..schemas import CourseReadSchema, CourseUpdateSchema

class UpdateCourseUseCaseProtocol(UseCaseProtocol[CourseReadSchema]):
    async def __call__(self, course_id: UUID, course_data: CourseUpdateSchema) -> CourseReadSchema:
        ...

class UpdateCourseUseCase(UpdateCourseUseCaseProtocol):
    def __init__(self, course_service: CourseServiceProtocol):
        self.course_service = course_service
    
    async def __call__(self, course_id: UUID, course_data: CourseUpdateSchema) -> CourseReadSchema:
        return await self.course_service.update(course_id, course_data)