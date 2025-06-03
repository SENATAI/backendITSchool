from fastapi import UploadFile
from uuid import UUID
from typing import Optional
import json
from school_site.core.use_cases import UseCaseProtocol
from ..services.courses import CourseServiceProtocol
from ..schemas import CourseWithPhotoReadSchema, CourseUpdateSchema

class UpdateCourseUseCaseProtocol(UseCaseProtocol[CourseWithPhotoReadSchema]):
    async def __call__(self, course_id: UUID, course_data: CourseUpdateSchema) -> CourseWithPhotoReadSchema:
        ...

class UpdateCourseUseCase(UpdateCourseUseCaseProtocol):
    def __init__(self, course_service: CourseServiceProtocol):
        self.course_service = course_service
    
    async def __call__(self, course_id: UUID, course_data: str, image: Optional[UploadFile]) -> CourseWithPhotoReadSchema:
        course = CourseUpdateSchema(**json.loads(course_data))
        return await self.course_service.update(course_id, course, image)