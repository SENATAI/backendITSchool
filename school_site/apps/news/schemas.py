from school_site.core.schemas import BaseModel, CreateBaseModel, UpdateBaseModel
from .enums import NewsStatus
from uuid import UUID

class NewsCreateSchema(CreateBaseModel):
    name: str
    description: str
    status: NewsStatus 


class NewsReadSchema(BaseModel):
    id: UUID
    name: str
    description: str
    status: NewsStatus  


class NewsUpdateSchema(UpdateBaseModel):
    id: UUID
    name: str
    description: str
    status: NewsStatus    

