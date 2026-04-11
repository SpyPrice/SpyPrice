from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import cards as cards_repository
from app.models import TrackingItem, PriceSnapshot

from urllib.parse import urlparse


def get_normalize_url(url: str) -> str:
    """Возвращает url без параметров запроса"""
    parsed = urlparse(url)
    return f'{parsed.scheme}://{parsed.netloc}{parsed.path}'


def get_base_url(url: str) -> str:
    """Возвращает базовый url (для source_url)"""
    parsed = urlparse(url)
    return f'{parsed.scheme}://{parsed.netloc}'


async def parse_new_card_from_etl() -> TrackingItem | None:
    print(NotImplementedError('\n\nСвязь с ETL ещё не налажена\n\n'))
    return None

async def add_watch(url: str, user_id: int, db: AsyncSession) -> bool | None:
    """
    True - карточка успешно добавлена к отслеживаемым,
    False - карточка уже отслеживается,
    None - не удалось добавить карточку к отслеживаемым
    """

    source_id = await cards_repository.get_source_id(get_base_url(url), db)

    if source_id is not None:
        card = await cards_repository.get_card_by_url(get_normalize_url(url), db)

        if card is not None:
            is_watched = await cards_repository.check_user_card_watch(user_id, card.id, db)
            if is_watched:
                return False
            else:
                await cards_repository.user_watch_card_add(user_id, card.id, db)
                await db.commit()
                return True
        else:
            card = await parse_new_card_from_etl()
            if card is not None:
                card = await cards_repository.create_card(
                    url = get_normalize_url(card.url),
                    name = card.name,
                    is_in_stock = card.is_in_stock,
                    source_id = source_id,
                    db=db
                )
                await cards_repository.user_watch_card_add(user_id, card.id, db)
                await db.commit()
                return True
            return None
    else:
        return None
