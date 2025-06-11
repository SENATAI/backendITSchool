from fastapi import APIRouter, Response, Depends
from uuid import UUID
from typing import List

from .schemas import (
    NewsCreateSchema,
    NewsReadSchema,
    NewsUpdateSchema,
    PaginationResultSchema,
    NewsUpdateRequestSchema
)
from .services.news import NewsService
from .depends import (
    get_news_service,
    get_create_news_use_case,
    get_delete_news_use_case,
    get_get_all_news_use_case,
    get_get_news_use_case,
    get_update_news_use_case
)
from .use_cases.create_news import CreateNewsUseCaseProtocol
from .use_cases.delete_news import DeleteNewsUseCaseProtocol
from .use_cases.get_all_news import GetAllNewsUseCaseProtocol
from .use_cases.get_news_by_id import GetNewsUseCaseProtocol
from .use_cases.update_news import UpdateNewsUseCaseProtocol

router = APIRouter(prefix='/api/news', tags=['News'])

@router.post('/', response_model=NewsReadSchema)
async def create_news(
    news_data: NewsCreateSchema,
    create_news_use_case: CreateNewsUseCaseProtocol = Depends(get_create_news_use_case)
) -> NewsReadSchema:
    return await create_news_use_case(news_data)

@router.get('/', response_model=PaginationResultSchema[NewsReadSchema])
async def get_all_news(
    news_service: NewsService = Depends(get_news_service)
) -> PaginationResultSchema[NewsReadSchema]:
    return await news_service.get_all_news()

@router.get('/{news_id}', response_model=NewsReadSchema)
async def get_news_by_id(
    news_id: UUID,
    get_news_use_case: GetNewsUseCaseProtocol = Depends(get_get_news_use_case)
) -> NewsReadSchema:
    return await get_news_use_case(news_id)

@router.put('/{news_id}', response_model=NewsReadSchema)
async def update_news(
    news_id: UUID,
    news_data: NewsUpdateRequestSchema,
    update_news_use_case: UpdateNewsUseCaseProtocol = Depends(get_update_news_use_case)
) -> NewsReadSchema:
    return await update_news_use_case(news_id, news_data)
    
@router.delete('/{news_id}')
async def delete_news(
    news_id: UUID,
    delete_news_use_case: DeleteNewsUseCaseProtocol = Depends(get_delete_news_use_case)
) -> Response:
    return await delete_news_use_case(news_id)