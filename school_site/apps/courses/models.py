from uuid import uuid4
from sqlalchemy import Column, String, Integer, Enum, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from school_site.core.db import Base
from school_site.core.models import TimestampMixin
from .enums import AgeCategory

class Course(Base, TimestampMixin):
    __tablename__ = "courses"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    age_category = Column(Enum(AgeCategory), nullable=False)
    price = Column(Integer, nullable=True)
    author_name = Column(String, nullable=True)

    __table_args__ = (
        CheckConstraint("price IS NULL OR price >= 0", name="positive_price_check"),
    )