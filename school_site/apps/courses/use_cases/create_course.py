from school_site.core.use_cases import UseCaseProtocol
from ..services.courses import CourseServiceProtocol
from ..schemas import CourseReadSchema, CourseCreateSchema

class CreateCourseUseCaseProtocol(UseCaseProtocol[CourseReadSchema]):
    async def __call__(self, course_data: CourseCreateSchema) -> CourseReadSchema:
        ...

class CreateCourseUseCase(CreateCourseUseCaseProtocol):
    def __init__(self, course_service: CourseServiceProtocol):
        self.course_service = course_service
    
    async def __call__(self, course_data: CourseCreateSchema) -> CourseReadSchema:
        return await self.course_service.create(course_data)