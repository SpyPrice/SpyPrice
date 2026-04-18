
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependency import get_async_session

from app.repository import metadata as metadata_repository
from app.schemas import SourceRead, TagRead


async def get_all_active_sources(db: AsyncSession):
    sources = await metadata_repository.get_all_active_sources(db)
    return list(map(SourceRead.model_validate, sources))


async def get_all_tags(db: AsyncSession):
    tags = await metadata_repository.get_all_tags(db)
    return list(map(TagRead.model_validate, tags))
