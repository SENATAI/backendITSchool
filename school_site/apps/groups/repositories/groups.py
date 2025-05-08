import sqlalchemy as sa
from sqlalchemy.sql.expression import func
from collections.abc import Iterable
from typing import Self, List
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.core.schemas import PaginationSchema
from ..models import Group, group_student
from ..schemas import (
    GroupCreateDBSchema,
    GroupReadDBSchema,
    GroupUpdateDBSchema,
    GroupDBPaginationResultSchema,
    GroupReadDBHeadSchema,
    GroupAddStudentsDBSchema
)


class GroupRepositoryProtocol(BaseRepositoryImpl[
    Group,
    GroupReadDBSchema,
    GroupCreateDBSchema,
    GroupUpdateDBSchema
]):
    async def paginate(
        self: Self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema
    ) -> GroupDBPaginationResultSchema:
        ...

    async def add_students(self, group_id: UUID, students: GroupAddStudentsDBSchema) -> None:
        ...

    async def delete_student(self, group_id: UUID, student_id: UUID) -> None:
        ...


class GroupRepository(GroupRepositoryProtocol):
    async def paginate(
        self: Self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema
    ) -> GroupDBPaginationResultSchema:
        async with self.session as s:
            statement = sa.select(self.model_type.id, self.model_type.name)

            if search:
                search_conditions = [
                    getattr(self.model_type, field).ilike(f"%{search}%")
                    for field in search_by
                ]
                statement = statement.where(sa.or_(*search_conditions))

            order_by_expr = self.get_order_by_expr(sorting)
            statement = statement.order_by(*order_by_expr)
            statement = statement.limit(pagination.limit).offset(pagination.offset)

            results = (await s.execute(statement)).all()
            
            count_statement = sa.select(func.count(self.model_type.id))
            if search:
                count_statement = count_statement.where(sa.or_(*search_conditions))
            count = (await s.execute(count_statement)).scalar_one()
            
            return GroupDBPaginationResultSchema(
                count=count,
                objects=[
                    GroupReadDBHeadSchema(id=id, name=name)
                    for id, name in results
                ]
            )

    async def add_students(self, group_id: UUID, students: GroupAddStudentsDBSchema) -> None:
        async with self.session as s:
            for student_id in students.students_id:
                statement = sa.insert(group_student).values(
                    group_id=group_id,
                    student_id=student_id
                )
                await s.execute(statement)
            await s.commit()

    async def delete_student(self, group_id: UUID, student_id: UUID) -> None:
        async with self.session as s:
            statement = sa.delete(group_student).where(
                sa.and_(
                    group_student.c.group_id == group_id,
                    group_student.c.student_id == student_id
                )
            )
            await s.execute(statement)
            await s.commit() 