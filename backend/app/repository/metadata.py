from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, Tuple, select

from app.models import Source, Tag


async def get_all_active_sources(db: AsyncSession) -> Sequence[tuple[int, str, str]]:
    query = (
        select(Source.id, Source.name, Source.url)
        .where(Source.is_collected == True)
    )
    result = await db.execute(query)
    return result.all()


async def get_all_tags(db: AsyncSession) -> Sequence[tuple[int, str, str]]:
    query = (
        select(Tag.id, Tag.name, Tag.description)
    )
    result = await db.execute(query)
    return result.all()
