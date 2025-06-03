from fastapi import UploadFile
from typing import Optional
import json
from school_site.core.use_cases import UseCaseProtocol
from ..services.courses import CourseServiceProtocol
from ..schemas import CourseWithPhotoReadSchema, CourseCreateSchema

class CreateCourseUseCaseProtocol(UseCaseProtocol[CourseWithPhotoReadSchema]):
    async def __call__(self, course_data: CourseCreateSchema) -> CourseWithPhotoReadSchema:
        ...

class CreateCourseUseCase(CreateCourseUseCaseProtocol):
    def __init__(self, course_service: CourseServiceProtocol):
        self.course_service = course_service
    
    async def __call__(self, course_data: str, image: Optional[UploadFile]) -> CourseWithPhotoReadSchema:
        course = CourseCreateSchema(**json.loads(course_data))

        return await self.course_service.create(course, image)