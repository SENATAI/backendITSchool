from fastapi import UploadFile
from typing import Optional
from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol 
from school_site.core.schemas import CursorPaginationWithSearchSchema
from ..services.products import ProductServiceProtocol 
from ..schemas import ProductCursorPaginationResultSchema 


class GetListProductUseCaseProtocol(UseCaseProtocol[ProductCursorPaginationResultSchema]):
    async def __call__(self, search: Optional[str],
                       search_by: Optional[list[str]],
                       cursor: Optional[UUID],
                       limit: int = 10) -> ProductCursorPaginationResultSchema:
        ...


class GetListProductUseCase(GetListProductUseCaseProtocol):
    def __init__(self, product_service: ProductServiceProtocol):
        self.product_service = product_service
    
    async def __call__(self, search: Optional[str],
                       search_by: Optional[list[str]],
                       cursor: Optional[UUID],
                       limit: int = 10) -> ProductCursorPaginationResultSchema:
        pagination = CursorPaginationWithSearchSchema(
            search=search,
            search_by=search_by,
            cursor=cursor,
            limit=limit
        )
        return await self.product_service.list(pagination)
