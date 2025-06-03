from uuid import uuid4
from sqlalchemy import Column, String, Integer, Enum, CheckConstraint, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from school_site.core.db import Base
from sqlalchemy.orm import relationship
from datetime import timezone
from school_site.core.models import TimestampMixin, FileMixin
from .enums import AgeCategory

class Course(Base, TimestampMixin):
    __tablename__ = "courses"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, nullable=False)
    photo = relationship("Photo", back_populates="course_photo", uselist=False, cascade="all, delete-orphan")

    description = Column(String, nullable=False)
    age_category = Column(Enum(AgeCategory), nullable=False)
    price = Column(Integer, nullable=True)
    author_name = Column(String, nullable=True)

    __table_args__ = (
        CheckConstraint("price IS NULL OR price >= 0", name="positive_price_check"),
    )

class Photo(Base, TimestampMixin, FileMixin):
    __tablename__ = "photo_courses"

    course_id = Column(PostgresUUID(as_uuid=True), ForeignKey("courses.id"), unique=True)

    course = relationship("Course", back_populates="photo_course")


class Lesson(Base, TimestampMixin):
    __tablename__ = "lessons"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    course_id = Column(PostgresUUID(as_uuid=True), ForeignKey("courses.id"), unique=True)

    course = relationship("Course", back_populates="lessons")
    groups = relationship("LessonGroup", back_populates="lesson")
    teacher_material_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lesson_html_files.id"))
    student_material_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lesson_html_files.id"))
    homework_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lesson_html_files.id"))

    teacher_material = relationship("LessonHtmlFile", foreign_keys=[teacher_material_id])
    student_material = relationship("LessonHtmlFile", foreign_keys=[student_material_id])
    homework = relationship("LessonHtmlFile", foreign_keys=[homework_id])

class LessonHtmlFile(Base, TimestampMixin, FileMixin):
    __tablename__ = "lesson_html_files"


class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    text = Column(String, nullable=False)
    date_created = Column(DateTime, default=timezone.utc)
    lesson_student_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lesson_students.id"))
    teacher_id = Column(
        PostgresUUID(as_uuid=True), 
        ForeignKey("teachers.id", ondelete="CASCADE"), 
        nullable=False
    )
    teacher = relationship("Teacher", back_populates="comments")

class Homework(Base):
    __tablename__ = "homeworks"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    date_created = Column(DateTime, default=timezone.utc)
    file_id = Column(PostgresUUID(as_uuid=True), ForeignKey("file_homeworks.id"))
    student_id = Column(
        PostgresUUID(as_uuid=True), 
        ForeignKey("students.id", ondelete="CASCADE"), 
        nullable=False
    )

    file = relationship("FileHomework")


class FileHomework(FileMixin, Base):
    __tablename__ = "file_homeworks"

    homework_id = Column(PostgresUUID(as_uuid=True), ForeignKey("homeworks.id"), unique=True)

    homework = relationship("Homework", back_populates="file_homework")

class LessonGroup(Base):
    __tablename__ = "lesson_groups"
    
    lesson_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lessons.id"), primary_key=True)
    group_id = Column(PostgresUUID(as_uuid=True), ForeignKey("groups.id"), primary_key=True)
    holding_date = Column(DateTime, nullable=False)
    is_opened = Column(PostgresUUID, default=False)
    
    lesson = relationship("Lesson", back_populates="groups")
    group = relationship("Group", back_populates="lessons")


class LessonStudent(Base):
    __tablename__ = "lesson_students"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id = Column(PostgresUUID(as_uuid=True), ForeignKey("students.id"))
    lesson_group_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lesson_groups.id"))
    is_visited = Column(Boolean, default=False)
    is_excused_absence = Column(Boolean, default=False)
    is_sent_homework = Column(Boolean, default=False)
    is_graded_homework = Column(Boolean, default=False)
    coins_for_visit = Column(Integer, default=0)
    coins_for_homework = Column(Integer, default=0)
    
    student = relationship("Student", back_populates="lessons")
    lesson_group = relationship("LessonGroup", back_populates="students")
    passed_homeworks = relationship("Homework", secondary="lesson_student_homework", back_populates="students")
    comments = relationship("Comment", back_populates="lesson_student")


class LessonStudentHomework(Base):
    __tablename__ = "lesson_student_homework"
    
    lesson_student_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lesson_students.id"), primary_key=True)
    homework_id = Column(PostgresUUID(as_uuid=True), ForeignKey("homeworks.id"), primary_key=True)


class CourseStudent(Base):
    __tablename__ = "course_students"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id = Column(PostgresUUID(as_uuid=True), ForeignKey("students.id"))
    course_id = Column(PostgresUUID(as_uuid=True), ForeignKey("courses.id"))
    progress = Column(PostgresUUID, default=0.0)
    
    student = relationship("Student", back_populates="courses")
    course = relationship("Course", back_populates="students")