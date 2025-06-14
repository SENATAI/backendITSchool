from typing import Self

from school_site.apps.news.schemas import NewsCreateSchema, NewsReadSchema
from school_site.apps.news.services.news import NewsServiceProtocol
from school_site.core.use_cases import UseCaseProtocol


class CreateNewsUseCaseProtocol(UseCaseProtocol[NewsReadSchema]):
    async def __call__(self, news: NewsCreateSchema) -> NewsReadSchema:
        ...

class CreateNewsUseCase(CreateNewsUseCaseProtocol):
    def __init__(self: Self, news_service: NewsServiceProtocol):
        self.news_service = news_service

    async def __call__(self: Self, news: NewsCreateSchema) -> NewsReadSchema:
        return await self.news_service.create_news(news)