from typing import List, Protocol, Self
from datetime import datetime
from uuid import UUID
from school_site.core.enums import UserRole
from school_site.core.utils.exceptions import ValidationError
from ..schemas import ScheduleReadSchema
from ..services.schedule import ScheduleServiceProtocol
from school_site.apps.users.services.auth import AuthServiceProtocol

class GetFilteredScheduleUseCaseProtocol(Protocol):
    async def __call__(
        self: Self,
        access_token: str,
        date_start: datetime,
        date_end: datetime
    ) -> List[ScheduleReadSchema]:
        ...

class GetFilteredScheduleUseCase(GetFilteredScheduleUseCaseProtocol):
    def __init__(self: Self, schedule_service: ScheduleServiceProtocol, auth_service: AuthServiceProtocol):
        self.schedule_service = schedule_service
        self.auth_service = auth_service

    async def __call__(
        self: Self,
        access_token: str,
        date_start: datetime,
        date_end: datetime
    ) -> List[ScheduleReadSchema]:
        token_data = await self.auth_service.decode_acess_token(access_token)
        if token_data.role == UserRole.STUDENT:
            return await self.schedule_service.get_filtered_student_schedule(
                token_data.user_id,
                date_start,
                date_end
            )
        elif token_data.role == UserRole.TEACHER:
            return await self.schedule_service.get_filtered_teacher_schedule(
                token_data.user_id,
                date_start,
                date_end
            )
        else:
            return await self.schedule_service.get_filtered_all_groups_schedule(
                date_start,
                date_end
            ) 