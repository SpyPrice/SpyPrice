from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import cards as cards_repository
from decimal import Decimal

from urllib.parse import urlparse

from app.api.backend_etl_api_connect import notify_etl_to_parse_new_item

from app.schemas import ItemRead, ShortPriceSnapshot, ShortSourceRead, PriceStatistics
from app.models import TrackingItem


def get_normalize_url(url: str) -> str:
    """Возвращает url без параметров запроса"""
    parsed = urlparse(url)
    return f'{parsed.scheme}://{parsed.netloc}{parsed.path}'.strip('/')


def get_base_url(url: str) -> str:
    """Возвращает базовый url (для source_url)"""
    parsed = urlparse(url)
    return f'{parsed.scheme}://{parsed.netloc}'.strip('/')


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
    await notify_etl_to_parse_new_item(norm_url, user_id, source_id)
    return 'pending'


async def create_card_and_watch(user_id: int, url: str, name: str, is_in_stock: bool | None,
                                source_id: int, db: AsyncSession) -> int:
    new_card = await cards_repository.create_card(get_normalize_url(url), name, is_in_stock, source_id, db)
    await cards_repository.user_watch_card_add(user_id, new_card.id, db)
    await db.commit()
    return new_card.id


async def create_price_snapshot(item_id: int, price: Decimal, currency: str | None, db: AsyncSession) -> int:
    new_price_snapshot = await cards_repository.create_price_snapshot(item_id, price, currency, db)
    await db.commit()
    return new_price_snapshot.id


async def generate_item_read(item_id: int, db: AsyncSession) -> ItemRead | None:
    item = await cards_repository.get_card_by_id(item_id, db)
    if item is None:
        return None
    snapshots = await cards_repository.get_card_last_and_week_snapshot(item_id, db)
    source = await cards_repository.get_source_by_id(item.source_id, db)

    last_row = snapshots.get('last')
    old_row = snapshots.get('old')
    last_snapshot = ShortPriceSnapshot(
        price=last_row.price,
        time=last_row.created_at
    ) if last_row else None
    snapshot_7_days_ago = ShortPriceSnapshot(
        price=old_row.price,
        time=old_row.created_at
    ) if old_row else None

    return ItemRead(
        id=item_id,
        name=item.name,
        url=item.url,
        is_in_stock=item.is_in_stock,
        currency='RUB',  # Пока заглушка, потом поменять логику работы с currency
        last_snapshot=last_snapshot,
        snapshot_7_days_ago=snapshot_7_days_ago,
        source=ShortSourceRead(
            id=source.id,
            name=source.name
        ),
        tags=[]  # Пока заглушка, потом поменять логику tags
    )


async def get_all_users_cards_with_snapshots(user_id: int, db: AsyncSession) -> list[ItemRead]:
    result: list[ItemRead] = []
    user_tracking_cards = await cards_repository.get_user_cards(user_id, db)
    for tracking_cards in user_tracking_cards:
        item_read = await generate_item_read(tracking_cards.tracking_item_id, db)
        if item_read is not None:
            result.append(item_read)
    return result


async def get_card_by_id(card_id: int, db: AsyncSession) -> TrackingItem | None:
    return await cards_repository.get_card_by_id(card_id, db)


async def get_all_snapshots(card_id: int, db: AsyncSession) -> list[ShortPriceSnapshot]:
    all_snapshots = await cards_repository.get_card_snapshots(card_id, db)
    converted = [ShortPriceSnapshot(price=snapshot.price, time=snapshot.created_at) for snapshot in all_snapshots]
    return converted


async def get_price_statistics(price_snapshots: list[ShortPriceSnapshot], db: AsyncSession) -> PriceStatistics:
    return PriceStatistics(
        min_price=min(price_snapshots, key=lambda price_snapshot: price_snapshot.price),
        max_price=max(price_snapshots, key=lambda price_snapshot: price_snapshot.price),
        avg_price=sum([price_snapshot.price for price_snapshot in price_snapshots]) / len(price_snapshots)
    )
