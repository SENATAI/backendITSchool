from school_site.core.use_cases import UseCaseProtocol
from ..services.courses import CourseServiceProtocol
from ..schemas import CoursePaginationResultSchema
from school_site.core.schemas import PaginationSchema

class GetListCoursesUseCaseProtocol(UseCaseProtocol[CoursePaginationResultSchema]):
    async def __call__(self, 
                       limit: int = 10, 
                       offset: int = 0) -> CoursePaginationResultSchema:
        ...

class GetListCoursesUseCase(GetListCoursesUseCaseProtocol):
    def __init__(self, course_service: CourseServiceProtocol):
        self.course_service = course_service
    
    async def __call__(self, 
                       limit: int = 10, 
                       offset: int = 0) -> CoursePaginationResultSchema:
        pagination = PaginationSchema(
            limit=limit, 
            offset=offset
            )
        return await self.course_service.list(pagination)