import sqlalchemy as sa
from sqlalchemy.sql.expression import func
from collections.abc import Iterable
from typing import Self
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.core.schemas import PaginationSchema
from ..models import Course
from ..schemas import (
    CourseCreateDBSchema,
    CourseReadDBSchema,
    CourseUpdateDBSchema,
    CourseDBPaginationResultSchema,
    CourseReadDBHeadSchema
)


class CourseRepositoryProtocol(BaseRepositoryImpl[
    Course,
    CourseReadDBSchema,
    CourseCreateDBSchema,
    CourseUpdateDBSchema
]):
    async def paginate(
        self: Self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema
    ) -> CourseDBPaginationResultSchema:
        ...


class CourseRepository(CourseRepositoryProtocol):
    async def paginate(
        self: Self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema
    ) -> CourseDBPaginationResultSchema:
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
            
            return CourseDBPaginationResultSchema(
                count=count,
                objects=[
                    CourseReadDBHeadSchema(id=id, name=name)
                    for id, name in results
                ]
            )
