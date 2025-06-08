from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from school_site.core.services.files import FileServiceProtocol
from school_site.core.depends import get_image_service
from school_site.apps.students.depends import get_student_by_group_service
from school_site.apps.students.services.students import StudentsByGroupServiceProtocol
from school_site.apps.users.services.auth import TokenServiceProtocol
from school_site.apps.users.depends import get_token_service
from .repositories.photo_courses import PhotoRepositoryProtocol, PhotoRepository
from .repositories.courses import CourseRepositoryProtocol, CourseRepository
from .repositories.lessons import LessonRepositoryProtocol, LessonRepository
from .repositories.lesson_html_files import LessonHTMLRepositoryProtocol, LessonHTMLRepository
from .repositories.lesson_group import LessonGroupRepositoryProtocol, LessonGroupRepository
from .repositories.lesson_student import LessonStudentRepositoryProtocol, LessonStudentRepository
from .services.lesson_group_student import CombinedLessonGroupStudentServiceProtocol, CombinedLessonGroupStudentService
from .services.photo_courses import PhotoServiceProtocol, PhotoService
from .services.courses import CourseServiceProtocol, CourseService
from .services.lessons import LessonServiceProtocol, LessonService
from .services.lesson_group import LessonGroupServiceProtocol, LessonGroupService
from .services.lesson_student import LessonStudentServiceProtocol, LessonStudentService
from .services.lesson_html_files import LessonHTMLServiceProtocol, LessonHTMLService
from .services.auth import AuthService, AuthAdminServiceProtocol
from .use_cases.courses.create_course import CreateCourseUseCaseProtocol, CreateCourseUseCase
from .use_cases.courses.update_course import UpdateCourseUseCaseProtocol, UpdateCourseUseCase
from .use_cases.courses.get_course import GetCourseUseCaseProtocol, GetCourseUseCase
from .use_cases.courses.delete_course import DeleteCourseUseCaseProtocol, DeleteCourseUseCase
from .use_cases.courses.list_courses import GetListCoursesUseCaseProtocol, GetListCoursesUseCase
from .use_cases.lessons.create_lesson import CreateLessonUseCaseProtocol, CreateLessonUseCase
from .use_cases.lessons.update_lesson import UpdateLessonUseCaseProtocol, UpdateLessonUseCase
from .use_cases.lessons.get_lesson import GetLessonUseCaseProtocol, GetLessonUseCase
from .use_cases.lessons.delete_lesson import DeleteLessonUseCaseProtocol, DeleteLessonUseCase
from .use_cases.lessons.list_lessons import GetListLessonsUseCaseProtocol, GetListLessonsUseCase
from .use_cases.materials.create_material import CreateLessonHTMLFileUseCaseProtocol, CreateLessonHTMLFileUseCase
from .use_cases.materials.update_material import UpdateLessonHTMLFileUseCaseProtocol, UpdateLessonHTMLFileUseCase
from .use_cases.materials.get_material import GetLessonHTMLFileUseCaseProtocol, GetLessonHTMLFileUseCase
from .use_cases.materials.delete_material import DeleteLessonHTMLFileUseCaseProtocol, DeleteLessonHTMLFileUseCase
from .use_cases.lesson_group_student.create_lesson_group_student import CreateLessonGroupStudentUseCaseProtocol, CreateLessonGroupStudentUseCase
from .use_cases.lesson_group_student.bulk_create_lesson_group_student import BulkCreateLessonGroupStudentUseCaseProtocol, BulkCreateLessonGroupStudentUseCase

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


def __get_lesson_group_repository(
        session: AsyncSession = Depends(get_async_session)
) -> LessonGroupRepositoryProtocol:
    return LessonGroupRepository(session)

def __get_lesson_student_repository(
    session: AsyncSession = Depends(get_async_session)
) -> LessonStudentRepositoryProtocol:
    return LessonStudentRepository(session)

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

def get_material_update_use_case(lesson_service: LessonHTMLServiceProtocol = Depends(get_lesson_html_service),
                                 auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
                                 ) -> UpdateLessonHTMLFileUseCaseProtocol:
    return UpdateLessonHTMLFileUseCase(lesson_service, auth_service)


def get_material_get_use_case(lesson_service: LessonHTMLServiceProtocol = Depends(get_lesson_html_service),
                                auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
                                 ) -> GetLessonHTMLFileUseCaseProtocol:
    return GetLessonHTMLFileUseCase(lesson_service, auth_service)

def get_material_delete_use_case(lesson_service: LessonHTMLServiceProtocol = Depends(get_lesson_html_service),
                                auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
                                 ) -> DeleteLessonHTMLFileUseCaseProtocol:
    return DeleteLessonHTMLFileUseCase(lesson_service, auth_service)
    

def get_lesson_group_service(repository: LessonGroupRepositoryProtocol = Depends(__get_lesson_group_repository)
                              ) -> LessonGroupServiceProtocol:
    return LessonGroupService(repository)

def get_lesson_student_service(repository: LessonStudentRepositoryProtocol = Depends(__get_lesson_student_repository)
                               ) -> LessonStudentServiceProtocol:
    return LessonStudentService(repository)

def get_combined_lesson_student_group_service(lesson_group_service: LessonGroupServiceProtocol = Depends(get_lesson_group_service),
                                              lesson_student_service: LessonStudentServiceProtocol = Depends(get_lesson_student_service),
                                              student_service: StudentsByGroupServiceProtocol = Depends(get_student_by_group_service)
                                              ) -> CombinedLessonGroupStudentServiceProtocol:
    return CombinedLessonGroupStudentService(lesson_group_service, lesson_student_service, student_service)

def get_create_lesson_group_student_use_case(lesson_student_group_service: CombinedLessonGroupStudentService = Depends(get_combined_lesson_student_group_service),
                                             auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
                                             ) -> CreateLessonGroupStudentUseCaseProtocol:
    return CreateLessonGroupStudentUseCase(lesson_student_group_service, auth_service) 

def get_bulk_create_lesson_group_student_use_case(lesson_student_group_service: CombinedLessonGroupStudentService = Depends(get_combined_lesson_student_group_service),
                                             auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
                                             ) -> BulkCreateLessonGroupStudentUseCaseProtocol:
    return BulkCreateLessonGroupStudentUseCase(lesson_student_group_service, auth_service)