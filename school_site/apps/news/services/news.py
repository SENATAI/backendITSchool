import logging 
from typing import Protocol
from ..repositories.news import NewsRepositoryProtocol
from ..schemas import (
    NewsCreateSchema,   
    NewsReadSchema, 
    NewsUpdateSchema,
    PaginationResultSchema,
    NewsUpdateRequestSchema
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

    async def get_all_news(self, limit: int = 10, offset: int = 0) -> PaginationResultSchema[NewsReadSchema]: 
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
        logger.info(f"Creating news with name {news.name} and with a pinned state {news.is_pinned}")

        exisitng_news = await self._get_news_by_name(news.name)
        if exisitng_news:
            logger.error(f"News with name {news.name} already exists")
            raise NewsAlreadyExistsError()
        
        news_create = NewsCreateSchema(
            name=news.name,
            description=news.description,
            is_pinned=news.is_pinned  
        )
        
        news_create = await self.news_repository.create(news_create)

        logger.info(f"Created news with name {news.name} and with a pinned state {news.is_pinned}")
        return NewsReadSchema(**news_create.model_dump())
    
    async def get_all_news(self: Self, limit: int = 10, offset: int = 0) -> PaginationResultSchema[NewsReadSchema]:
        logger.info(f"Getting all news with limit={limit}, offset={offset}")
        paginated_news = await self.news_repository.get_all(limit=limit, offset=offset)
        
        # Преобразуем SQLAlchemy модели в Pydantic модели
        news_schemas = [NewsReadSchema.model_validate(news, from_attributes=True) for news in paginated_news.objects]
    
        
        # Создаем PaginationResultSchema с помощью model_validate
        return PaginationResultSchema[NewsReadSchema].model_validate({
            "count": paginated_news.count,
            "objects": news_schemas
            })
    
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
    
    async def update_news(self, news_id: UUID, news_data: NewsUpdateRequestSchema) -> NewsReadSchema:
        logger.info(f"Fetching news with id {news_id}")
        existing_news = await self.news_repository.get(news_id)
    
        if not existing_news:
            logger.info(f"News to update with id {news_id} not found")
            raise NewsNotFoundException()
        
        # Создаем NewsUpdateSchema с id из URL
        update_data = NewsUpdateSchema(
            id=news_id,
            name=news_data.name,
            description=news_data.description,
            is_pinned=news_data.is_pinned
        )

        updated_news = await self.news_repository.update(update_data)

        return NewsReadSchema(**updated_news.model_dump())



    
    async def delete_news(self, news_id: UUID) -> bool:
        logger.info(f"Fetching news with id {news_id}")
        news_to_delete = await self.news_repository.get(news_id)
        if not news_to_delete:
            logger.info(f"News to delete with id {news_id} not found")
            raise NewsNotFoundException()
        
        logger.info(f"Deleting news with id {news_id}")
        return await self.news_repository.delete(news_id)
       