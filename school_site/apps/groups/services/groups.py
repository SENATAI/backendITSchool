import logging
from typing import Protocol
from uuid import UUID
from school_site.core.schemas import PaginationSchema
from ..schemas import (
    GroupCreateSchema,
    GroupUpdateSchema,
    GroupReadSchema,
    GroupReadHeadSchema,
    GroupPaginationResultSchema,
    GroupCreateDBSchema
)
from ..repositories.groups import GroupRepositoryProtocol


logger = logging.getLogger(__name__)


class GroupServiceProtocol(Protocol):
    async def create(self, group: GroupCreateSchema) -> GroupReadSchema:
        ...

    async def get(self, group_id: UUID) -> GroupReadSchema:
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
            description=group.description
        )
        new_group = await self.group_repository.create(group_db)
        return GroupReadSchema(
            id=new_group.id,
            name=new_group.name,
            description=new_group.description
        )

    async def get(self, group_id: UUID) -> GroupReadSchema:
        group = await self.group_repository.get(group_id)
        return GroupReadSchema(
            id=group.id,
            name=group.name,
            description=group.description
        )

    async def update(self, group_id: UUID, group: GroupUpdateSchema) -> GroupReadSchema:
        updated_group = await self.group_repository.update(group)
        return GroupReadSchema(
            id=updated_group.id,
            name=updated_group.name,
            description=updated_group.description
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