from .repositories.news import NewsRepository
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from .repositories.news import NewsRepositoryProtocol
from .services.news import NewsService 
from .use_cases.create_news import CreateNewsUseCaseProtocol, CreateNewsUseCase
from .services.news import NewsServiceProtocol
from .use_cases.get_news_by_id import GetNewsUseCaseProtocol, GetNewsUseCase
from .use_cases.update_news import UpdateNewsUseCaseProtocol, UpdateNewsUseCase
from .use_cases.delete_news import DeleteNewsUseCaseProtocol, DeleteNewsUseCase
from .use_cases.get_all_news import GetAllNewsUseCaseProtocol, GetAllNewsUseCase

def __get_news_repository(session: AsyncSession = Depends(get_async_session)) -> NewsRepositoryProtocol:
    return NewsRepository(session)

def get_news_service(news_repository: NewsRepositoryProtocol = Depends(__get_news_repository)) -> NewsRepositoryProtocol:
    return NewsService(news_repository)

def get_create_news_use_case(news_service: NewsServiceProtocol = Depends(get_news_service)) -> CreateNewsUseCaseProtocol:
    return CreateNewsUseCase(news_service)

def get_get_news_use_case(news_service: NewsServiceProtocol = Depends(get_news_service)) -> GetNewsUseCaseProtocol:
    return GetNewsUseCase(news_service)

def get_update_news_use_case(news_service: NewsServiceProtocol = Depends(get_news_service)) -> UpdateNewsUseCaseProtocol:
    return  UpdateNewsUseCase(news_service)

def get_delete_news_use_case(news_service: NewsServiceProtocol = Depends(get_news_service)) -> DeleteNewsUseCaseProtocol:
    return  DeleteNewsUseCase(news_service)

def get_get_all_news_use_case(news_service: NewsServiceProtocol = Depends(get_news_service)) -> GetAllNewsUseCaseProtocol:
    return GetAllNewsUseCase(news_service)