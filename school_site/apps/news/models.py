from uuid import uuid4
from sqlalchemy import Column, String, Enum as SQLEnum, Boolean
from school_site.core.db import Base 
from school_site.core.models import TimestampMixin
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from .enums import NewsStatus


class News(Base, TimestampMixin):
    __tablename__ = 'news'
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    is_pinned = Column(Boolean)

__all__ = ["News"]