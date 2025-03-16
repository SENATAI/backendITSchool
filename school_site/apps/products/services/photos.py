import logging
from typing import Protocol
from uuid import UUID
from ..schemas import (
    PhotoCreateSchema,
    PhotoUpdateSchema,
    PhotoReadSchema
)
from ..repositories.products import ProductRepositoryProtocol
from ..repositories.photos import PhotoRepositoryProtocol

logger = logging.getLogger(__name__)


class PhotoServiceProtocol(Protocol):
    async def create(self, photo: PhotoCreateSchema) -> PhotoReadSchema:
        ...

    async def get(self, photo_id: UUID) -> PhotoReadSchema:
        ...

    async def update(self, photo_id: UUID, product: PhotoUpdateSchema) -> PhotoReadSchema:
        ...

    async def delete(self, photo_id: UUID) -> bool:
        ...


class PhotoService(PhotoServiceProtocol):
    def __init__(self, 
                 photo_repository: PhotoRepositoryProtocol,
                 ):
        self.photo_repository = photo_repository

    async def create(self, photo: PhotoCreateSchema) -> PhotoReadSchema:
        created_photo = await self.photo_repository.create(photo)
        return created_photo 

    async def get(self, photo_id: UUID) -> PhotoReadSchema:
        product = await self.photo_repository.get(photo_id)
        return product

    async def update(self, photo: PhotoCreateSchema) -> PhotoReadSchema:
        updated_photo = await self.photo_repository.update(photo)
        return updated_photo

    async def delete_product(self, photo_id: UUID) -> bool:
        return await self.photo_repository.delete(photo_id)
