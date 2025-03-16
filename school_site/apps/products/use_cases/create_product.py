from school_site.core.use_cases import UseCaseProtocol 
from ..services.products import ProductServiceProtocol 
from ..services.auth import AuthServiceProtocol
from ..schemas import ProductReadSchema, ProductCreateSchema

class CreateProductUseCaseProtocol(UseCaseProtocol[ProductReadSchema]):
    async def __call__(self, product: ProductCreateSchema) -> ProductReadSchema:
        ...


class CreateProductUseCase(CreateProductUseCaseProtocol):
    def __init__(self, auth_service: AuthServiceProtocol, product_service: ProductServiceProtocol):
        self.auth_service = auth_service
        self.product_service = product_service
    
    async def __call__(self, token: str, product: ProductCreateSchema) -> ProductReadSchema:
        await self.auth_service.get_admin_user(token)
        return await self.product_service.create(product)
