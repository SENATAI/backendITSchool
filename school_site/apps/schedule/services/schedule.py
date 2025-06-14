from typing import Self, List
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