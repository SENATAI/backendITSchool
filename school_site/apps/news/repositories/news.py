import sqlalchemy as sa

from ..models import News
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..schemas import NewsReadSchema, NewsCreateSchema, NewsUpdateSchema, PaginationResultSchema

class NewsRepositoryProtocol(BaseRepositoryImpl[News, NewsReadSchema, NewsCreateSchema, NewsUpdateSchema]):

    async def get_by_name(name: str) -> NewsReadSchema | None:
        ...

    async def get_all(limit: int, offset: int) -> PaginationResultSchema[NewsReadSchema]:
        ...

class NewsRepository(NewsRepositoryProtocol):
    async def get_by_name(self, name: str) -> NewsReadSchema | None:
        async with self.session as session:
            stmt = sa.select(self.model_type).where(self.model_type.name == name)
            news = (await session.execute(stmt)).scalar_one_or_none()
            if news is None:
                return None
            return self.read_schema_type.model_validate(news, from_attributes=True)
       
    async def get_all(self, limit: int = 10, offset: int = 0) -> PaginationResultSchema[NewsReadSchema]:
        async with self.session as session:
            count_query = sa.select(sa.func.count(self.model_type.id))
            total_count = (await session.execute(count_query)).scalar_one()
            
            data_query = (
                sa.select(self.model_type)
                .order_by(self.model_type.created_at.desc())  
                .limit(limit)
                .offset(offset)
            )
            models = (await session.execute(data_query)).scalars().all()
            
            # Преобразуем SQLAlchemy модели в Pydantic модели
            pydantic_models = [self.read_schema_type.model_validate(model, from_attributes=True) for model in models]

            return PaginationResultSchema[NewsReadSchema](
                count=total_count,
                objects=pydantic_models
            )