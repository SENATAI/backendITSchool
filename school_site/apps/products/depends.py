from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from .repositories.products import ProductRepositoryProtocol, ProductRepository
from .services.products import ProductServiceProtocol, ProductService
from .use_cases.create_product import CreateProductUseCaseProtocol, CreateProductUseCase
from .repositories.photos import PhotoRepositoryProtocol, PhotoRepository
from .services.photos import PhotoServiceProtocol, PhotoService
from .services.auth import AuthServiceProtocol, AuthService

def __get_photo_repository(
        session: AsyncSession = Depends(get_async_session)
) -> PhotoRepositoryProtocol:
    return PhotoRepository(session)


def __get_product_repository(
        session: AsyncSession = Depends(get_async_session)
) -> ProductRepositoryProtocol:
    return ProductRepository(session)


def get_photo_service(
        photo_repository: PhotoRepositoryProtocol = Depends(__get_photo_repository)
) -> PhotoServiceProtocol:
    return PhotoService(photo_repository)


def get_product_service(
        product_repository: ProductRepositoryProtocol = Depends(__get_product_repository),
        photo_service: PhotoServiceProtocol = Depends(get_photo_service) 
) -> ProductServiceProtocol:
    return ProductService(product_repository, photo_service)
    

def get_auth_service() -> AuthServiceProtocol:
    return AuthService()


def get_product_create_use_case(auth_service: AuthServiceProtocol = Depends(get_auth_service), 
                                product_service: ProductServiceProtocol = Depends(get_product_service)) -> \
        CreateProductUseCaseProtocol:
    return CreateProductUseCase(auth_service, product_service)