from typing import Self, List
from datetime import datetime
from school_site.core.use_cases import UseCaseProtocol
from ..schemas import ScheduleReadSchema
from ..repositories.schedule import ScheduleRepositoryProtocol
from school_site.core.enums import UserRole
from school_site.core.utils.exceptions import ValidationError

class ScheduleServiceProtocol(UseCaseProtocol[List[ScheduleReadSchema]]):
    async def get_student_schedule(self: Self, user_id: str) -> List[ScheduleReadSchema]:
        ...
    
    async def get_teacher_schedule(self: Self, user_id: str) -> List[ScheduleReadSchema]:
        ...

    async def get_filtered_student_schedule(
        self: Self,
        user_id: str,
        date_start: datetime,
        date_end: datetime
    ) -> List[ScheduleReadSchema]:
        ...

    async def get_filtered_teacher_schedule(
        self: Self,
        user_id: str,
        date_start: datetime,
        date_end: datetime
    ) -> List[ScheduleReadSchema]:
        ...

    async def get_all_groups_schedule(self: Self) -> List[ScheduleReadSchema]:
        ...

    async def get_filtered_all_groups_schedule(
        self: Self,
        date_start: datetime,
        date_end: datetime
    ) -> List[ScheduleReadSchema]:
        ...

class ScheduleService(ScheduleServiceProtocol):
    def __init__(
        self: Self,
        schedule_repository: ScheduleRepositoryProtocol,
    ):
        self.schedule_repository = schedule_repository

    async def get_student_schedule(self: Self, user_id: str) -> List[ScheduleReadSchema]:
        return await self.schedule_repository.get_student_schedule(user_id)

    async def get_teacher_schedule(self: Self, user_id: str) -> List[ScheduleReadSchema]:
        return await self.schedule_repository.get_teacher_schedule(user_id)

    async def get_filtered_student_schedule(
        self: Self,
        user_id: str,
        date_start: datetime,
        date_end: datetime
    ) -> List[ScheduleReadSchema]:
        return await self.schedule_repository.get_filtered_student_schedule(
            user_id,
            date_start,
            date_end
        )

    async def get_filtered_teacher_schedule(
        self: Self,
        user_id: str,
        date_start: datetime,
        date_end: datetime
    ) -> List[ScheduleReadSchema]:
        return await self.schedule_repository.get_filtered_teacher_schedule(
            user_id,
            date_start,
            date_end
        )

    async def get_all_groups_schedule(self: Self) -> List[ScheduleReadSchema]:
        return await self.schedule_repository.get_all_groups_schedule()

    async def get_filtered_all_groups_schedule(
        self: Self,
        date_start: datetime,
        date_end: datetime
    ) -> List[ScheduleReadSchema]:
        return await self.schedule_repository.get_filtered_all_groups_schedule(
            date_start,
            date_end
        ) 