import sqlalchemy as sa
from sqlalchemy.orm import joinedload
from uuid import UUID
from typing import Self
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.apps.products.models import Product
from school_site.apps.products.schemas import (
    ProductCreateDBSchema, ProductReadDBSchema, ProductUpdateDBSchema, ProductReadSchema
)
from school_site.core.utils.exceptions import ModelNotFoundException, SortingFieldNotFoundError


class ProductRepositoryProtocol(BaseRepositoryImpl[
    Product,
    ProductReadDBSchema,
    ProductCreateDBSchema,
    ProductUpdateDBSchema
]):
    async def get_with_photo(self: Self, id: UUID) -> ProductReadSchema:
        ...


class ProductRepository(ProductRepositoryProtocol):
    async def get_with_photo(self: Self, id: UUID) -> ProductReadSchema:
        async with self.session as s, s.begin():
            statement = (
                sa.select(self.model_type)
                .options(sa.orm.selectinload(self.model_type.photo)) 
                .where(self.model_type.id == id)
            )
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                raise ModelNotFoundException(self.model_type, id)
            return ProductReadSchema.model_validate(model, from_attributes=True)
