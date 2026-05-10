from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from app.repository import metadata as metadata_repository
from app.schemas import SourceRead, TagRead, ItemNotify, ShortPriceSnapshot

from app.repository import cards as cards_repository


async def get_all_active_sources(db: AsyncSession):
    sources = await metadata_repository.get_all_active_sources(db)
    return list(map(SourceRead.model_validate, sources))


async def get_all_tags(db: AsyncSession):
    tags = await metadata_repository.get_all_tags(db)
    return list(map(TagRead.model_validate, tags))


async def get_all_user_tags(user_id: int, db: AsyncSession):
    tags = await metadata_repository.get_all_user_tags(user_id, db)
    return list(map(TagRead.model_validate, tags))


async def get_all_notifications(user_id: int, db: AsyncSession):
    user_tracking_items = await cards_repository.get_user_cards(user_id, db)
    items = [await cards_repository.get_card_by_id(item.id, db) for item in user_tracking_items]

    notifications = []
    for item in items:
        notification = await create_card_notification(item.id, item.name, item.url,  db)
        print(notification)
        if notification and notification.delta >= 10:
            notifications.append(notification)
    return notifications


async def create_card_notification(card_id: int, card_name: str, card_url: str, db: AsyncSession) -> ItemNotify | None:
    try:
        price_snapshots = await metadata_repository.get_card_last_2_prices(card_id, db)
        price_snapshots = [ShortPriceSnapshot(price=snapshot.price, time=snapshot.created_at) for snapshot in price_snapshots]

        delta = (100 - price_snapshots[0].price * 100 / price_snapshots[1].price).quantize(Decimal('0.01'))

        return ItemNotify(
            id=card_id,
            name=card_name,
            url=card_url,
            delta=delta,
            last_snapshot=price_snapshots[0],
            penultimate_snapshot=price_snapshots[1],
            text=f'Цена понизилась на {delta}%! Текущая цена: {price_snapshots[0].price} Успей приобрести!'
        )
    except Exception as e:
        print(e)
        return None
