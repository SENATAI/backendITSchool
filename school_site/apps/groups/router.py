from fastapi import APIRouter, Depends, Path, Query
from uuid import UUID
from .use_cases.create_group import CreateGroupUseCaseProtocol
from .use_cases.update_group import UpdateGroupUseCaseProtocol
from .use_cases.get_group import GetGroupUseCaseProtocol
from .use_cases.delete_group import DeleteGroupUseCaseProtocol
from .use_cases.list_groups import GetListGroupsUseCaseProtocol
from .depends import (
    get_group_create_use_case, get_group_update_use_case, get_group_get_use_case,
    get_group_delete_use_case, get_group_get_list_use_case
)
from .schemas import GroupReadSchema, GroupPaginationResultSchema, GroupCreateSchema, GroupUpdateSchema

router = APIRouter(prefix='/api/groups', tags=['Groups'])


@router.post("/", response_model=GroupReadSchema, status_code=201)
async def create_group(
    group_data: GroupCreateSchema,
    create: CreateGroupUseCaseProtocol = Depends(get_group_create_use_case)
):
    created_group = await create(group_data)
    return created_group


@router.put("/{group_id}", response_model=GroupReadSchema, status_code=200)
async def update_group(
    group_data: GroupUpdateSchema,
    group_id: UUID = Path(...),
    update: UpdateGroupUseCaseProtocol = Depends(get_group_update_use_case)
):
    updated_group = await update(group_id, group_data)
    return updated_group


@router.get("/{group_id}", response_model=GroupReadSchema, status_code=200)
async def get_group(
    group_id: UUID = Path(...),
    get: GetGroupUseCaseProtocol = Depends(get_group_get_use_case)
):
    group = await get(group_id)
    return group


@router.get("/", response_model=GroupPaginationResultSchema, status_code=200)
async def list_groups(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0, le=100),
    list: GetListGroupsUseCaseProtocol = Depends(get_group_get_list_use_case)
):
    groups = await list(limit, offset)
    return groups


@router.delete("/{group_id}", status_code=204)
async def delete_group(
    group_id: UUID = Path(...),
    delete: DeleteGroupUseCaseProtocol = Depends(get_group_delete_use_case)
):
    await delete(group_id)
    return None
