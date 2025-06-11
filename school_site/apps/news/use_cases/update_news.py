from typing import Self
from uuid import UUID
from school_site.apps.news.schemas import NewsReadSchema, NewsUpdateSchema, NewsUpdateRequestSchema
from school_site.apps.news.services.news import NewsServiceProtocol
from school_site.core.use_cases import UseCaseProtocol

class UpdateNewsUseCaseProtocol(UseCaseProtocol[NewsReadSchema]):
    async def __call__(self: Self, news_id: UUID, news_data: NewsUpdateRequestSchema) -> NewsReadSchema:
        ...

class UpdateNewsUseCase(UpdateNewsUseCaseProtocol):
    def __init__(self: Self, news_service: NewsServiceProtocol):
        self.news_service = news_service

    async def __call__(self: Self, news_id: UUID, news_data: NewsUpdateRequestSchema) -> NewsReadSchema:
        return await self.news_service.update_news(news_id, news_data)