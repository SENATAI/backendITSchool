from school_site.core.schemas import BaseModel, CreateBaseModel, UpdateBaseModel
from .enums import NewsStatus
from uuid import UUID
from datetime import datetime
from typing import TypeVar, Generic, List

T = TypeVar('T')

class PaginationResultSchema(BaseModel, Generic[T]):
    count: int
    objects: List[T]

class NewsCreateSchema(CreateBaseModel):
    name: str
    description: str
    is_pinned: bool 


class NewsReadSchema(BaseModel):
    id: UUID
    name: str
    description: str
    is_pinned: bool 
    created_at: datetime
    updated_at: datetime 


class NewsUpdateSchema(UpdateBaseModel):
    id: UUID
    name: str
    description: str
    is_pinned: bool   


class NewsUpdateRequestSchema(BaseModel):
    name: str
    description: str
    is_pinned: bool

