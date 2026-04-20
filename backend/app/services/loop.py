from app.repository import cards as cards_repository

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.dependency import get_async_session


async def start_loop(db: AsyncSession = Depends(get_async_session)):
    cards = await cards_repository.get_all_cards_id_source_url(db)
    pass
