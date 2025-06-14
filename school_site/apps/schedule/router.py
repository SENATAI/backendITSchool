from fastapi import APIRouter, Depends
from typing import List
from .schemas import ScheduleReadSchema
from .use_cases.get_schedule import GetScheduleUseCaseProtocol
from .depends import get_schedule_use_case
from school_site.apps.users.depends import access_token_schema

router = APIRouter(prefix='/api/schedule', tags=['Schedule'])

@router.get('/', response_model=List[ScheduleReadSchema], status_code=200)
async def get_schedule(
    access_token: str = Depends(access_token_schema),
    get_schedule_use_case: GetScheduleUseCaseProtocol = Depends(get_schedule_use_case)
):
    return await get_schedule_use_case(access_token)
