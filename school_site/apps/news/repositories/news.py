import sqlalchemy as sa

from ..models import News
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..schemas import NewsReadSchema, NewsCreateSchema, NewsUpdateSchema

class NewsRepositoryProtocol(BaseRepositoryImpl[News, NewsReadSchema, NewsCreateSchema, NewsUpdateSchema]):

    async def get_by_name(name: str) -> NewsReadSchema | None:
        ...


class NewsRepository(NewsRepositoryProtocol):
    async def get_by_name(self, name: str) -> NewsReadSchema | None:
        async with self.session as session:
            stmt = sa.select(self.model_type).where(self.model_type.name == name)
            news = (await session.execute(stmt)).scalar_one_or_none()
            if news is None:
                return None
            return self.read_schema_type.model_validate(news, from_attributes=True)
       