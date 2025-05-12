import sqlalchemy as sa
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import group_student
from ..schemas import GroupAddStudentsDBSchema


class GroupStudentsRepositoryProtocol(BaseRepositoryImpl):
    async def add_students(self, group_id: UUID, students: GroupAddStudentsDBSchema) -> None:
        ...

    async def delete_student(self, group_id: UUID, student_id: UUID) -> None:
        ...


class GroupStudentsRepository(GroupStudentsRepositoryProtocol):
    async def add_students(self, group_id: UUID, students: GroupAddStudentsDBSchema) -> None:
        async with self.session as s, s.begin():
            for student_id in students.students_id:
                statement = sa.dialects.postgresql.insert(group_student).values(
                    group_id=group_id,
                    student_id=student_id
                ).on_conflict_do_nothing(
                    index_elements=['group_id', 'student_id']
                )
                await s.execute(statement)

    async def delete_student(self, group_id: UUID, student_id: UUID) -> None:
        async with self.session as s, s.begin():
            statement = sa.delete(group_student).where(
                sa.and_(
                    group_student.c.group_id == group_id,
                    group_student.c.student_id == student_id
                )
            )
            await s.execute(statement) 