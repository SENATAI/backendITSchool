import sqlalchemy as sa
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.apps.products.models import Photo
from school_site.apps.products.schemas import (
    PhotoCreateSchema, PhotoUpdateSchema, PhotoReadSchema
)

class PhotoRepositoryProtocol(BaseRepositoryImpl[
    Photo,
    PhotoReadSchema,
    PhotoCreateSchema,
    PhotoUpdateSchema
]):
    pass

class PhotoRepository(PhotoRepositoryProtocol):
    pass