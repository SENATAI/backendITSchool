from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from school_site.core.services.files import FileServiceProtocol
from school_site.core.depends import get_image_service
from school_site.apps.users.services.auth import TokenServiceProtocol
from school_site.apps.users.depends import get_token_service
from .repositories.photo_courses import PhotoRepositoryProtocol, PhotoRepository
from .repositories.courses import CourseRepositoryProtocol, CourseRepository
from .repositories.lessons import LessonRepositoryProtocol, LessonRepository
from .repositories.lesson_html_files import LessonHTMLRepositoryProtocol, LessonHTMLRepository
from .services.photo_courses import PhotoServiceProtocol, PhotoService
from .services.courses import CourseServiceProtocol, CourseService
from .services.lessons import LessonServiceProtocol, LessonService
from .services.lesson_html_files import LessonHTMLServiceProtocol, LessonHTMLService
from .services.auth import AuthService, AuthAdminServiceProtocol
from .use_cases.create_course import CreateCourseUseCaseProtocol, CreateCourseUseCase
from .use_cases.update_course import UpdateCourseUseCaseProtocol, UpdateCourseUseCase
from .use_cases.get_course import GetCourseUseCaseProtocol, GetCourseUseCase
from .use_cases.delete_course import DeleteCourseUseCaseProtocol, DeleteCourseUseCase
from .use_cases.list_courses import GetListCoursesUseCaseProtocol, GetListCoursesUseCase
from .use_cases.create_lesson import CreateLessonUseCaseProtocol, CreateLessonUseCase
from .use_cases.update_lesson import UpdateLessonUseCaseProtocol, UpdateLessonUseCase
from .use_cases.get_lesson import GetLessonUseCaseProtocol, GetLessonUseCase
from .use_cases.delete_lesson import DeleteLessonUseCaseProtocol, DeleteLessonUseCase
from .use_cases.list_lessons import GetListLessonsUseCaseProtocol, GetListLessonsUseCase
from .use_cases.create_material import CreateLessonHTMLFileUseCaseProtocol, CreateLessonHTMLFileUseCase


def get_course_file_service() -> FileServiceProtocol:
    """Зависимость для работы с изображениями продуктов."""
    return get_image_service("course-files")

def __get_photo_repository(
        session: AsyncSession = Depends(get_async_session)
) -> PhotoRepositoryProtocol:
    return PhotoRepository(session)


def __get_course_repository(
        session: AsyncSession = Depends(get_async_session)
) -> CourseRepositoryProtocol:
    return CourseRepository(session)


def __get_lesson_repository(
        session: AsyncSession = Depends(get_async_session)
) -> LessonRepositoryProtocol:
    return LessonRepository(session)

def __get_lesson_html_file_repository(
        session: AsyncSession = Depends(get_async_session)
) -> LessonHTMLRepositoryProtocol:
    return LessonHTMLRepository(session)


def get_photo_service(
        photo_repository: PhotoRepositoryProtocol = Depends(__get_photo_repository),
        image_service: FileServiceProtocol = Depends(get_course_file_service)
) -> PhotoServiceProtocol:
    return PhotoService(photo_repository, image_service)

def get_course_service(
        course_repository: CourseRepositoryProtocol = Depends(__get_course_repository),
        photo_service: PhotoServiceProtocol = Depends(get_photo_service)
) -> CourseServiceProtocol:
    return CourseService(course_repository, photo_service)

def get_lesson_service(
        lesson_repository: LessonRepositoryProtocol = Depends(__get_lesson_repository)
) -> LessonServiceProtocol:
    return LessonService(lesson_repository)

def get_auth_service(
    token_service: TokenServiceProtocol = Depends(get_token_service)
) -> AuthAdminServiceProtocol:
    return AuthService(token_service)

def get_course_create_use_case(
        course_service: CourseServiceProtocol = Depends(get_course_service),
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> CreateCourseUseCaseProtocol:
    return CreateCourseUseCase(course_service, auth_service)

def get_course_update_use_case(
        course_service: CourseServiceProtocol = Depends(get_course_service),
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> UpdateCourseUseCaseProtocol:
    return UpdateCourseUseCase(course_service, auth_service)

def get_course_get_use_case(
        course_service: CourseServiceProtocol = Depends(get_course_service)
) -> GetCourseUseCaseProtocol:
    return GetCourseUseCase(course_service)

def get_course_delete_use_case(
        course_service: CourseServiceProtocol = Depends(get_course_service),
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> DeleteCourseUseCaseProtocol:
    return DeleteCourseUseCase(course_service, auth_service)

def get_course_get_list_use_case(
        course_service: CourseServiceProtocol = Depends(get_course_service)
) -> GetListCoursesUseCaseProtocol:
    return GetListCoursesUseCase(course_service)

def get_lesson_create_use_case(
        lesson_service: LessonServiceProtocol = Depends(get_lesson_service),
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> CreateLessonUseCaseProtocol:
    return CreateLessonUseCase(lesson_service, auth_service)

def get_lesson_update_use_case(
        lesson_service: LessonServiceProtocol = Depends(get_lesson_service),
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> UpdateLessonUseCaseProtocol:
    return UpdateLessonUseCase(lesson_service, auth_service)

def get_lesson_get_use_case(
        lesson_service: LessonServiceProtocol = Depends(get_lesson_service)
) -> GetLessonUseCaseProtocol:
    return GetLessonUseCase(lesson_service)

def get_lesson_delete_use_case(
        lesson_service: LessonServiceProtocol = Depends(get_lesson_service),
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> DeleteLessonUseCaseProtocol:
    return DeleteLessonUseCase(lesson_service, auth_service)

def get_lesson_get_list_use_case(
        lesson_service: LessonServiceProtocol = Depends(get_lesson_service)
) -> GetListLessonsUseCaseProtocol:
    return GetListLessonsUseCase(lesson_service)

def get_lesson_html_service(
        lesson_html_repository = Depends(__get_lesson_html_file_repository),
        file_service: FileServiceProtocol = Depends(get_course_file_service)
                            ) -> LessonHTMLServiceProtocol:
    return LessonHTMLService(lesson_html_repository, file_service)

def get_material_create_use_case(lesson_service: LessonHTMLServiceProtocol = Depends(get_lesson_html_service),
                                 auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
                                 ) -> CreateLessonHTMLFileUseCaseProtocol:
    return CreateLessonHTMLFileUseCase(lesson_service, auth_service)