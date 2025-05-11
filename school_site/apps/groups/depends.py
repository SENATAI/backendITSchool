from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from .repositories.groups import GroupRepositoryProtocol, GroupRepository
from .repositories.group_students import GroupStudentsRepositoryProtocol, GroupStudentsRepository
from .services.groups import GroupServiceProtocol, GroupService
from .services.students import GroupStudentServiceProtocol, GroupStudentService
from .use_cases.create_group import CreateGroupUseCaseProtocol, CreateGroupUseCase
from .use_cases.update_group import UpdateGroupUseCaseProtocol, UpdateGroupUseCase
from .use_cases.get_group import GetGroupUseCaseProtocol, GetGroupUseCase
from .use_cases.delete_group import DeleteGroupUseCaseProtocol, DeleteGroupUseCase
from .use_cases.list_groups import GetListGroupsUseCaseProtocol, GetListGroupsUseCase
from .use_cases.add_students import AddStudentsUseCaseProtocol, AddStudentsUseCase
from .use_cases.delete_student import DeleteStudentUseCaseProtocol, DeleteStudentUseCase
from school_site.apps.students.services.students import StudentServiceProtocol
from school_site.apps.students.depends import get_students_services

def __get_group_repository(
        session: AsyncSession = Depends(get_async_session)
) -> GroupRepositoryProtocol:
    return GroupRepository(session)

def __get_group_students_repository(
        session: AsyncSession = Depends(get_async_session)
) -> GroupStudentsRepositoryProtocol:
    return GroupStudentsRepository(session)

def get_group_service(
        group_repository: GroupRepositoryProtocol = Depends(__get_group_repository)
) -> GroupServiceProtocol:
    return GroupService(group_repository)

def get_group_student_service(
    group_students_repository: GroupStudentsRepositoryProtocol = Depends(__get_group_students_repository),
    student_service: StudentServiceProtocol = Depends(get_students_services)
) -> GroupStudentServiceProtocol:
    return GroupStudentService(group_students_repository, student_service)

def get_group_create_use_case(
        group_service: GroupServiceProtocol = Depends(get_group_service)
) -> CreateGroupUseCaseProtocol:
    return CreateGroupUseCase(group_service)

def get_group_update_use_case(
        group_service: GroupServiceProtocol = Depends(get_group_service)
) -> UpdateGroupUseCaseProtocol:
    return UpdateGroupUseCase(group_service)

def get_group_get_use_case(
        group_service: GroupServiceProtocol = Depends(get_group_service)
) -> GetGroupUseCaseProtocol:
    return GetGroupUseCase(group_service)

def get_group_delete_use_case(
        group_service: GroupServiceProtocol = Depends(get_group_service)
) -> DeleteGroupUseCaseProtocol:
    return DeleteGroupUseCase(group_service)

def get_group_get_list_use_case(
        group_service: GroupServiceProtocol = Depends(get_group_service)
) -> GetListGroupsUseCaseProtocol:
    return GetListGroupsUseCase(group_service)

def get_add_students_use_case(
        student_service: GroupStudentServiceProtocol = Depends(get_group_student_service)
) -> AddStudentsUseCaseProtocol:
    return AddStudentsUseCase(student_service)

def get_delete_student_use_case(
        student_service: GroupStudentServiceProtocol = Depends(get_group_student_service)
) -> DeleteStudentUseCaseProtocol:
    return DeleteStudentUseCase(student_service)
