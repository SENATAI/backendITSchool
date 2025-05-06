import logging
from typing import Protocol
from uuid import UUID
from school_site.core.schemas import PaginationSchema
from ..schemas import (
    CourseCreateSchema,
    CourseUpdateSchema,
    CourseReadSchema,
    CourseReadHeadSchema,
    CoursePaginationResultSchema,
    CourseCreateDBSchema
)
from ..repositories.courses import CourseRepositoryProtocol


logger = logging.getLogger(__name__)


class CourseServiceProtocol(Protocol):
    async def create(self, course: CourseCreateSchema) -> CourseReadSchema:
        ...

    async def get(self, course_id: UUID) -> CourseReadSchema:
        ...

    async def update(self, course_id: UUID, course: CourseUpdateSchema) -> CourseReadSchema:
        ...

    async def delete(self, course_id: UUID) -> None:
        ...

    async def list(self, pagination: PaginationSchema) -> CoursePaginationResultSchema:
        ...


class CourseService(CourseServiceProtocol):
    def __init__(self, course_repository: CourseRepositoryProtocol):
        self.course_repository = course_repository

    async def create(self, course: CourseCreateSchema) -> CourseReadSchema:
        course_db = CourseCreateDBSchema(
            name=course.name,
            description=course.description,
            age_category=course.age_category,
            price=course.price,
            author_name=course.author_name
        )
        new_course = await self.course_repository.create(course_db)
        return CourseReadSchema(
            id=new_course.id,
            name=new_course.name,
            description=new_course.description,
            age_category=new_course.age_category,
            price=new_course.price,
            author_name=new_course.author_name
        )

    async def get(self, course_id: UUID) -> CourseReadSchema:
        course = await self.course_repository.get(course_id)
        return CourseReadSchema(
            id=course.id,
            name=course.name,
            description=course.description,
            age_category=course.age_category,
            price=course.price,
            author_name=course.author_name
        )

    async def update(self, course_id: UUID, course: CourseUpdateSchema) -> CourseReadSchema:
        updated_course = await self.course_repository.update(course)
        return CourseReadSchema(
            id=updated_course.id,
            name=updated_course.name,
            description=updated_course.description,
            age_category=updated_course.age_category,
            price=updated_course.price,
            author_name=updated_course.author_name
        )

    async def delete(self, course_id: UUID) -> None:
        await self.course_repository.delete(course_id)

    async def list(self, pagination: PaginationSchema) -> CoursePaginationResultSchema:
        courses_paginate = await self.course_repository.paginate(
            search=None,
            search_by=None,
            pagination=pagination,
            sorting=["created_at", "id"]
        )
        return CoursePaginationResultSchema(
            objects=[CourseReadHeadSchema(id=c.id, name=c.name) for c in courses_paginate.objects],
            count=courses_paginate.count
        )