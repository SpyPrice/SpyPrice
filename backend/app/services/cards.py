from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from app.repository import cards as cards_repository
from decimal import Decimal

from urllib.parse import urlparse


def get_normalize_url(url: str) -> str:
    """Возвращает url без параметров запроса"""
    parsed = urlparse(url)
    return f'{parsed.scheme}://{parsed.netloc}{parsed.path}'


def get_base_url(url: str) -> str:
    """Возвращает базовый url (для source_url)"""
    parsed = urlparse(url)
    return f'{parsed.scheme}://{parsed.netloc}'


async def add_watch(url: str, user_id: int, db: AsyncSession) -> str:
    source_id = await cards_repository.get_source_id(get_base_url(url), db)

    if source_id is None:
        return 'source_not_supported'

    norm_url = get_normalize_url(url)
    card = await cards_repository.get_card_by_url(norm_url, db)

    if card is not None:
        is_watched = await cards_repository.check_user_card_watch(user_id, card.id, db)
        if is_watched:
            return 'already_watched'
        await cards_repository.user_watch_card_add(user_id, card.id, db)
        await db.commit()
        return 'success'

    # Карточки нет -> отправляем запрос в ETL на создание
    await notify_etl_to_parse(norm_url, user_id)
    return 'pending'


async def notify_etl_to_parse(url: str, user_id: int):
    # Потом брать из ENV
    etl_url = 'http://127.0.0.1:8000/ask_parse'
    callback_url = 'http://127.0.0.1:8000/webhook/etl-add-item-parse-result'
    print(f'{url=}, {user_id=}')
    async with AsyncClient() as client:
        try:
            m = await client.post(etl_url, json={
                'url': url,
                'user_id': user_id,
                'callback_url': callback_url
            })
            if m.status_code != 200:
                raise Exception(m.status_code)
        except Exception as e:
            print('\n'*3 + f'ошибка связи с ETL: {e}' + '\n'*3)


async def create_card_and_watch(user_id: int, url: str, name: str, is_in_stock: bool | None,
                                source_id: int, db: AsyncSession) -> int:
    new_card = await cards_repository.create_card(url, name, is_in_stock, source_id, db)
    await cards_repository.user_watch_card_add(user_id, new_card.id, db)
    await db.commit()
    return new_card.id


async def create_price_snapshot(item_id: int, price: Decimal, currency: str | None, db: AsyncSession) -> int:
    new_price_snapshot = await cards_repository.create_price_snapshot(item_id, price, currency, db)
    await db.commit()
    return new_price_snapshot.id
