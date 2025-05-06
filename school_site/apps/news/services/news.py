import logging 
from typing import Protocol
from ..repositories.news import NewsRepositoryProtocol
from ..schemas import (
    NewsCreateSchema,   
    NewsReadSchema, 
    NewsUpdateSchema
)

from uuid import UUID
from ..exceptions import NewsAlreadyExistsError, NewsNotFoundException
from ..enums import NewsStatus
from typing_extensions import Self

logger = logging.getLogger(__name__)


class NewsServiceProtocol(Protocol): 

    async def create_news(self, news: NewsCreateSchema) -> NewsReadSchema: 
        ...

    async def get_news_by_id(self, news_id: UUID) -> NewsReadSchema: 
        ... 

    async def get_all_news(self) -> list[NewsReadSchema]: 
        ... 

    async def _get_news_by_name(self, name: str) -> NewsReadSchema | None:
        ...

    async def update_news(self, news_id: UUID) -> NewsReadSchema:
        ...

    async def delete_news(self, news_id: UUID) -> bool:
        ...

        
class NewsService(NewsServiceProtocol):
    def __init__(self: Self, news_repository: NewsRepositoryProtocol):
        self.news_repository = news_repository

    async def create_news(self: Self, news: NewsCreateSchema) -> NewsReadSchema:
        logger.info(f"Creating news with name {news.name} and status {news.status}")

        exisitng_news = await self._get_news_by_name(news.name)
        if exisitng_news:
            logger.error(f"News with name {news.name} already exists")
            raise NewsAlreadyExistsError()
        
        news_create = NewsCreateSchema(
            name=news.name,
            description=news.description,
            status=NewsStatus(news.status)  
        )
        
        news_create = await self.news_repository.create(news_create)

        logger.info(f"Created news with name {news.name} and status {news.status}")
        return NewsReadSchema(**news_create.model_dump())
    
    async def get_all_news(self: Self) -> list[NewsReadSchema]:
        logger.info("Getting all news")
        news = await self.news_repository.get_all()
        return [NewsReadSchema(**news.model_dump()) for news in news]
    
    async def get_news_by_id(self: Self, news_id: UUID) -> NewsReadSchema:   
        logger.info(f"Fetching news with id {news_id}")
        news = await self.news_repository.get(news_id)
        if not news:
            logger.error(f"News with id {news_id} not found")
            raise NewsNotFoundException()
        return NewsReadSchema(**news.model_dump())
    
    async def _get_news_by_name(self, name: str) -> NewsReadSchema | None:
        news = await self.news_repository.get_by_name(name)
        return news
    
    async def update_news(self, news_id: UUID, news_data: NewsUpdateSchema) -> NewsReadSchema:
        logger.info(f"Fetching news with id {news_id}")
        existing_news = await self.news_repository.get(news_id)
    
        if not existing_news:
            logger.info(f"News to update with id {news_id} not found")
            raise NewsNotFoundException()

        # Теперь у нас есть id в news_data, можем его использовать
        # Если в схеме id совпадает с news_id, его можно просто использовать
        if news_data.id != news_id:
            raise ValueError("The id in the data does not match the provided news_id")

        # Обновляем новость с помощью данных из request
        updated_news = await self.news_repository.update(news_data)

        return NewsReadSchema(**updated_news.model_dump())



    
    async def delete_news(self, news_id: UUID) -> bool:
        logger.info(f"Fetching news with id {news_id}")
        news_to_delete = await self.news_repository.get(news_id)
        if not news_to_delete:
            logger.info(f"News to delete with id {news_id} not found")
            raise NewsNotFoundException()
        
        logger.info(f"Deleting news with id {news_id}")
        return await self.news_repository.delete(news_id)
       