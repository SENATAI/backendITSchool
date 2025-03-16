import logging
from typing import Protocol
from uuid import UUID
from ..schemas import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductUpdateDBSchema,
    ProductReadSchema,
    ProductReadDBSchema,
    ProductCreateDBSchema,
    PhotoCreateSchema,
    PhotoUpdateSchema
)
from ..repositories.products import ProductRepositoryProtocol
from .photos import PhotoServiceProtocol

logger = logging.getLogger(__name__)


class ProductServiceProtocol(Protocol):
    async def create(self, product: ProductCreateSchema) -> ProductReadSchema:
        ...

    async def get(self, product_id: UUID) -> ProductReadDBSchema:
        ...

    async def update(self, product_id: UUID, product: ProductUpdateDBSchema) -> ProductReadSchema:
        ...

    async def delete(self, product_id: UUID) -> bool:
        ...


class ProductService(ProductServiceProtocol):
    def __init__(self, product_repository: ProductRepositoryProtocol,
                 photo_service: PhotoServiceProtocol):
        self.product_repository = product_repository
        self.photo_service = photo_service

    async def create(self, product: ProductCreateSchema) -> ProductReadSchema:
        product_db = ProductCreateDBSchema(
            name=product.name,
            description=product.description,
            price=product.price
        )

        new_product = await self.product_repository.create(product_db)
        
        if product.photo:
            await self.photo_service.create(
                PhotoCreateSchema(name=product.photo.name, product_id=new_product.id)
            )
        created_product = await self.get_with_photo(new_product.id)
        return created_product
    

    async def get(self, product_id: UUID) -> ProductReadDBSchema:
        product = await self.product_repository.get(product_id)
        return product


    async def get_with_photo(self, product_id: UUID) -> ProductReadSchema:
        product = await self.product_repository.get_with_photo(product_id)
        return product


    async def update(self, product: ProductUpdateSchema) -> ProductReadSchema:
        upd_product_db = ProductUpdateDBSchema(
            name=product.name,
            description=product.description,
            price=product.price
        )
        updated_product = await self.product_repository.update(upd_product_db)
        if product.photo:
            await self.photo_service.update(
                PhotoUpdateSchema(
                    id=product.photo.id,
                    product_id=updated_product.id,
                    name=product.photo.name
                )
            )

        return await self.get_with_photo(updated_product.id)

    async def delete_product(self, product_id: UUID) -> bool:
        return await self.product_repository.delete(product_id)
