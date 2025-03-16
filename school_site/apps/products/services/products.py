from fastapi import UploadFile
import logging
from typing import Protocol, Optional
from uuid import UUID
from ..schemas import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductUpdateDBSchema,
    ProductReadSchema,
    ProductCursorPaginationResultSchema,
    ProductCreateDBSchema,
    PhotoCreateSchema,
    PhotoUpdateSchema,
    ProductWithPhotoDBReadSchema,
    PhotoReadSchema
)
from school_site.core.schemas import CursorPaginationWithSearchSchema, CursorPaginationResultSchema
from ..repositories.products import ProductRepositoryProtocol
from .photos import PhotoServiceProtocol

logger = logging.getLogger(__name__)


class ProductServiceProtocol(Protocol):
    async def create(self, product: ProductCreateSchema, image: Optional[UploadFile]) -> ProductReadSchema:
        ...

    async def get(self, product_id: UUID) -> ProductReadSchema:
        ...

    async def update(self, product_id: UUID, product: ProductUpdateSchema, image: Optional[UploadFile]) -> ProductReadSchema:
        ...

    async def delete(self, product_id: UUID) -> bool:
        ...

    async def list(self, pagination: CursorPaginationWithSearchSchema) -> ProductCursorPaginationResultSchema:
        ...


class ProductService(ProductServiceProtocol):
    def __init__(self, product_repository: ProductRepositoryProtocol,
                 photo_service: PhotoServiceProtocol):
        self.product_repository = product_repository
        self.photo_service = photo_service

    async def create(self, product: ProductCreateSchema, image: Optional[UploadFile]) -> ProductReadSchema:
        product_db = ProductCreateDBSchema(
            name=product.name,
            description=product.description,
            price=product.price
        )

        new_product = await self.product_repository.create(product_db)
        
        photo = None
        if product.photo and image:
            photo = await self.photo_service.create(
                PhotoCreateSchema(name=product.photo.name, product_id=new_product.id),
                image
            )

        return ProductReadSchema(
            id=new_product.id,
            name=new_product.name,
            description=new_product.description,
            price=new_product.price,
            photo=photo
        )
    

    async def get(self, product_id: UUID) -> ProductReadSchema:
        product = await self.product_repository.get_with_photo(product_id)
        image_url = await self.photo_service.get_photo_url(product.photo.path)
        return ProductReadSchema(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            created_at=product.created_at,
            updated_at=product.updated_at,
            photo=PhotoReadSchema(
                name=product.photo.name,
                product_id=product.id,
                url=image_url,
                created_at=product.photo.created_at,
                updated_at=product.photo.updated_at
            )
        )


    async def get_with_photo(self, product_id: UUID) -> ProductWithPhotoDBReadSchema:
        product = await self.product_repository.get_with_photo(product_id)
        return product


    async def update(self, product_id: UUID, product: ProductUpdateSchema, image: Optional[UploadFile]) -> ProductReadSchema:
        upd_product_db = ProductUpdateDBSchema(
            id=product_id,
            name=product.name,
            description=product.description,
            price=product.price
        )
        updated_product = await self.product_repository.update(upd_product_db)
        photo = None
        
        if product.photo and image:
            photo_id = product.photo.id or ((await self.get_with_photo(product_id)).photo.id)
            photo = await self.photo_service.update(
                photo_id,
                PhotoUpdateSchema(
                    product_id=product_id,
                    name=product.photo.name
                ),
                image
            )

        return ProductReadSchema(
            id=updated_product.id,
            name=updated_product.name,
            description=updated_product.description,
            price=updated_product.price,
            created_at=updated_product.created_at,
            photo=photo,
        )

    async def delete(self, product_id: UUID) -> bool:
        product = await self.get_with_photo(product_id)
        await self.photo_service.delete(product.photo.id)
        return await self.product_repository.delete(product_id)
    
    async def list(self, pagination: CursorPaginationWithSearchSchema) -> ProductCursorPaginationResultSchema:
        return await self.product_repository.cursor_paginate(
            search=pagination.search,
            search_by=pagination.search_by,
            cursor=pagination.cursor,
            limit=pagination.limit,
            sorting=["created_at", "id"]
        )
