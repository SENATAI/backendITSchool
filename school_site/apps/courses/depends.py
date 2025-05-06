from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from .repositories.courses import CourseRepositoryProtocol, CourseRepository
from .services.courses import CourseServiceProtocol, CourseService
from .use_cases.create_course import CreateCourseUseCaseProtocol, CreateCourseUseCase
from .use_cases.update_course import UpdateCourseUseCaseProtocol, UpdateCourseUseCase
from .use_cases.get_course import GetCourseUseCaseProtocol, GetCourseUseCase
from .use_cases.delete_course import DeleteCourseUseCaseProtocol, DeleteCourseUseCase
from .use_cases.list_courses import GetListCoursesUseCaseProtocol, GetListCoursesUseCase

def __get_course_repository(
        session: AsyncSession = Depends(get_async_session)
) -> CourseRepositoryProtocol:
    return CourseRepository(session)

def get_course_service(
        course_repository: CourseRepositoryProtocol = Depends(__get_course_repository)
) -> CourseServiceProtocol:
    return CourseService(course_repository)

def get_course_create_use_case(
        course_service: CourseServiceProtocol = Depends(get_course_service)
) -> CreateCourseUseCaseProtocol:
    return CreateCourseUseCase(course_service)

def get_course_update_use_case(
        course_service: CourseServiceProtocol = Depends(get_course_service)
) -> UpdateCourseUseCaseProtocol:
    return UpdateCourseUseCase(course_service)

def get_course_get_use_case(
        course_service: CourseServiceProtocol = Depends(get_course_service)
) -> GetCourseUseCaseProtocol:
    return GetCourseUseCase(course_service)

def get_course_delete_use_case(
        course_service: CourseServiceProtocol = Depends(get_course_service)
) -> DeleteCourseUseCaseProtocol:
    return DeleteCourseUseCase(course_service)

def get_course_get_list_use_case(
        course_service: CourseServiceProtocol = Depends(get_course_service)
) -> GetListCoursesUseCaseProtocol:
    return GetListCoursesUseCase(course_service)
