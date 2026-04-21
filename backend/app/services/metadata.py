from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import metadata as metadata_repository
from app.schemas import SourceRead, TagRead


async def get_all_active_sources(db: AsyncSession):
    sources = await metadata_repository.get_all_active_sources(db)
    return list(map(SourceRead.model_validate, sources))


async def get_all_tags(db: AsyncSession):
    tags = await metadata_repository.get_all_tags(db)
    return list(map(TagRead.model_validate, tags))


async def get_all_user_tags(user_id: int, db: AsyncSession):
    tags = await metadata_repository.get_all_user_tags(user_id, db)
    return list(map(TagRead.model_validate, tags))
