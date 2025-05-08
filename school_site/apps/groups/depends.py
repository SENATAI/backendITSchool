from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from .repositories.groups import GroupRepositoryProtocol, GroupRepository
from .services.groups import GroupServiceProtocol, GroupService
from .use_cases.create_group import CreateGroupUseCaseProtocol, CreateGroupUseCase
from .use_cases.update_group import UpdateGroupUseCaseProtocol, UpdateGroupUseCase
from .use_cases.get_group import GetGroupUseCaseProtocol, GetGroupUseCase
from .use_cases.delete_group import DeleteGroupUseCaseProtocol, DeleteGroupUseCase
from .use_cases.list_groups import GetListGroupsUseCaseProtocol, GetListGroupsUseCase

def __get_group_repository(
        session: AsyncSession = Depends(get_async_session)
) -> GroupRepositoryProtocol:
    return GroupRepository(session)

def get_group_service(
        group_repository: GroupRepositoryProtocol = Depends(__get_group_repository)
) -> GroupServiceProtocol:
    return GroupService(group_repository)

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
