import logging
from typing import Protocol
from uuid import UUID
from school_site.core.schemas import PaginationSchema
from ..schemas import (
    GroupCreateSchema,
    GroupUpdateSchema,
    GroupUpdateDBSchema,
    GroupReadSchema,
    GroupReadHeadSchema,
    GroupPaginationResultSchema,
    GroupCreateDBSchema,
    GroupWithStudentsAndTeacherAndCoursesSchema
)
from ..repositories.groups import GroupRepositoryProtocol


logger = logging.getLogger(__name__)


class GroupServiceProtocol(Protocol):
    async def create(self, group: GroupCreateSchema) -> GroupReadSchema:
        ...

    async def get(self, group_id: UUID) -> GroupWithStudentsAndTeacherAndCoursesSchema:
        ...

    async def update(self, group_id: UUID, group: GroupUpdateSchema) -> GroupReadSchema:
        ...

    async def delete(self, group_id: UUID) -> None:
        ...

    async def list(self, pagination: PaginationSchema) -> GroupPaginationResultSchema:
        ...


class GroupService(GroupServiceProtocol):
    def __init__(self, group_repository: GroupRepositoryProtocol):
        self.group_repository = group_repository

    async def create(self, group: GroupCreateSchema) -> GroupReadSchema:
        group_db = GroupCreateDBSchema(
            name=group.name,
            description=group.description,
            start_date=group.start_date,
            end_date=group.end_date,
            teacher_id=group.teacher_id
        )
        new_group = await self.group_repository.create(group_db)
        return GroupReadSchema(
            id=new_group.id,
            name=new_group.name,
            description=new_group.description,
            start_date=new_group.start_date,
            end_date=new_group.end_date,
            teacher_id=new_group.teacher_id
        )

    async def get(self, group_id: UUID) -> GroupWithStudentsAndTeacherAndCoursesSchema:
        group = await self.group_repository.get_with_students_and_teacher(group_id)
        return group

    async def update(self, group_id: UUID, group: GroupUpdateSchema) -> GroupReadSchema:
        group_db = GroupUpdateDBSchema(
            id=group_id,
            name=group.name,
            description=group.description,
            start_date=group.start_date,
            end_date=group.end_date,
            teacher_id=group.teacher_id
        )
        updated_group = await self.group_repository.update(group_db)
        return GroupReadSchema(
            id=updated_group.id,
            name=updated_group.name,
            description=updated_group.description,
            start_date=updated_group.start_date,
            end_date=updated_group.end_date,
            teacher_id=updated_group.teacher_id
        )

    async def delete(self, group_id: UUID) -> None:
        await self.group_repository.delete(group_id)

    async def list(self, pagination: PaginationSchema) -> GroupPaginationResultSchema:
        groups_paginate = await self.group_repository.paginate(
            search=None,
            search_by=None,
            pagination=pagination,
            sorting=["created_at", "id"]
        )
        return GroupPaginationResultSchema(
            objects=[GroupReadHeadSchema(id=g.id, name=g.name) for g in groups_paginate.objects],
            count=groups_paginate.count
        ) 