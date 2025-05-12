import sqlalchemy as sa
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import Group
from ..schemas import GroupAddTeacherDBSchema


class GroupTeachersRepositoryProtocol(BaseRepositoryImpl):
    async def add_teacher(self, group_id: UUID, teacher: GroupAddTeacherDBSchema) -> None:
        ...

    async def delete_teacher(self, group_id: UUID) -> None:
        ...

    async def has_teacher(self, group_id: UUID) -> bool:
        ...


class GroupTeachersRepository(GroupTeachersRepositoryProtocol):
    async def add_teacher(self, group_id: UUID, teacher: GroupAddTeacherDBSchema) -> None:
        async with self.session as s, s.begin():
            statement = sa.update(Group).where(
                Group.id == group_id
            ).values(
                teacher_id=teacher.teacher_id
            )
            await s.execute(statement)

    async def delete_teacher(self, group_id: UUID) -> None:
        async with self.session as s, s.begin():
            statement = sa.update(Group).where(
                Group.id == group_id
            ).values(
                teacher_id=None
            )
            await s.execute(statement)

    async def has_teacher(self, group_id: UUID) -> bool:
        async with self.session as s:
            statement = sa.select(Group.teacher_id).where(Group.id == group_id)
            result = await s.execute(statement)
            teacher_id = result.scalar_one_or_none()
            return teacher_id is not None 