import sqlalchemy as sa
from sqlalchemy.sql.expression import func
from collections.abc import Iterable
from typing import Self, Any
from uuid import UUID
from school_site.core.utils.exceptions import ModelNotFoundException
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.core.schemas import PaginationSchema
from ..models import Course
from ..schemas import (
    CourseCreateDBSchema,
    CourseReadDBSchema,
    CourseUpdateDBSchema,
    CourseWithPhotoReadDBSchema,
    CourseWithPhotoPaginationResultDBSchema
)


class CourseRepositoryProtocol(BaseRepositoryImpl[
    Course,
    CourseReadDBSchema,
    CourseCreateDBSchema,
    CourseUpdateDBSchema
]):
    async def get_with_photo(self: Self, id: UUID) -> CourseWithPhotoReadDBSchema:
        ...

    async def paginate(
        self: Self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema,
        user: Any,
        policies: list[str],
    )  -> CourseWithPhotoPaginationResultDBSchema:
        ...


class CourseRepository(CourseRepositoryProtocol):

    async def get_with_photo(self: Self, id: UUID) -> CourseWithPhotoReadDBSchema:
        async with self.session as s, s.begin():
            statement = (
                sa.select(self.model_type)
                .options(sa.orm.selectinload(self.model_type.photo)) 
                .where(self.model_type.id == id)
            )
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                raise ModelNotFoundException(self.model_type, id)
            return CourseWithPhotoReadDBSchema.model_validate(model, from_attributes=True)


    async def paginate(
        self: Self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema,
        user: Any,
        policies: list[str],
    ) -> CourseWithPhotoPaginationResultDBSchema:
        if len(policies) == 0:
            return CourseWithPhotoPaginationResultDBSchema(objects=[], count=0)
        async with self.session as s:
            statement = sa.select(self.model_type).options(sa.orm.selectinload(self.model_type.photo)) 
            if search:
                search_where: sa.ColumnElement[Any] = sa.false()
                for sb in search_by:
                    search_where = sa.or_(search_where, getattr(self.model_type, sb).ilike(f'%{search}%'))
                statement = statement.where(search_where)
            order_by_expr = self.get_order_by_expr(sorting)
            models = (
                (await s.execute(statement.limit(pagination.limit).offset(pagination.offset).order_by(*order_by_expr)))
                .scalars()
                .all()
            )
            objects = [CourseWithPhotoReadDBSchema.model_validate(model, from_attributes=True) for model in models]
            count_statement = statement.with_only_columns(func.count(self.model_type.id))
            count = (await s.execute(count_statement)).scalar_one()
            return CourseWithPhotoPaginationResultDBSchema(count=count, objects=objects)
  