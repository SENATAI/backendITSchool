from uuid import uuid4
from sqlalchemy import Column, String, Table, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from school_site.core.db import Base
from school_site.core.models import TimestampMixin
import sqlalchemy as sa


group_student = Table(
    "group_student",
    Base.metadata,
    Column("group_id", PostgresUUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE")),
    Column("student_id", PostgresUUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE")),
    sa.UniqueConstraint('group_id', 'student_id', name='uq_group_student')
)

class Group(Base, TimestampMixin):
    __tablename__ = "groups"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    teacher_id = Column(PostgresUUID(as_uuid=True), ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    students = relationship("Student", secondary=group_student, back_populates="groups")
    teacher = relationship("Teacher", back_populates="groups")
    lessons = relationship("LessonGroup", back_populates="group")

__all__ = ["group_student", "Group"]