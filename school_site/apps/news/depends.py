from .repositories.news import NewsRepository
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from .repositories.news import NewsRepositoryProtocol
from .services.news import NewsService 


def __get_news_repository(session: AsyncSession = Depends(get_async_session)) -> NewsRepositoryProtocol:
    return NewsRepository(session)

def get_news_service(news_repository: NewsRepositoryProtocol = Depends(__get_news_repository)) -> NewsRepositoryProtocol:
    return NewsService(news_repository)

