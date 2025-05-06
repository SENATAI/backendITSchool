from fastapi import APIRouter, Response, Depends
from uuid import UUID
from typing import List

from .schemas import (
    NewsCreateSchema,
    NewsReadSchema,
    NewsUpdateSchema
)
from .services.news import NewsService
from .depends import get_news_service

router = APIRouter(prefix='/api/news', tags=['News'])

@router.post('/', response_model=NewsReadSchema)
async def create_news(
    news_data: NewsCreateSchema,
    news_service: NewsService = Depends(get_news_service)
) -> NewsReadSchema:
    return await news_service.create_news(news_data)

@router.get('/', response_model=List[NewsReadSchema])
async def get_all_news(
    news_service: NewsService = Depends(get_news_service)
) -> List[NewsReadSchema]:
    return await news_service.get_all_news()

@router.get('/{news_id}', response_model=NewsReadSchema)
async def get_news_by_id(
    news_id: UUID,
    news_service: NewsService = Depends(get_news_service)
) -> NewsReadSchema:
    return await news_service.get_news_by_id(news_id)

@router.put('/{news_id}', response_model=NewsReadSchema)
async def update_news(
    news_id: UUID,
    news_data: NewsUpdateSchema,
    news_service: NewsService = Depends(get_news_service)
) -> NewsReadSchema:
    news_data.id = news_id
    return await news_service.update_news(news_data)
    
@router.delete('/{news_id}')
async def delete_news(
    news_id: UUID,
    news_service: NewsService = Depends(get_news_service)
) -> Response:
    return await news_service.delete_news(news_id)