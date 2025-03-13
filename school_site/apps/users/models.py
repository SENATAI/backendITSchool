from datetime import datetime
from uuid import uuid4
from school_site.core.db import Base
from school_site.core.models import CreationTimeMixin, TimestampMixin
from school_site.core.enums import UserRole
from sqlalchemy import Column, ForeignKey, String, Enum
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship

class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(UserRole))
    
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")

class RefreshToken(Base, CreationTimeMixin):
    __tablename__ = "refresh_tokens"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    hashed_refresh_token = Column(String, index=True)
    
    user = relationship("User", back_populates="refresh_tokens")