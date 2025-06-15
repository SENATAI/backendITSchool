from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from school_site.core.schemas import TimestampMixin

class ScheduleReadSchema(BaseModel):
    id: UUID
    lesson_id: UUID
    group_id: UUID
    holding_date: datetime
    is_opened: bool
    lesson_name: str
    course_name: str

    class Config:
        from_attributes = True 