from app.models import TrackingItem, UsersTrackingItem, Source, PriceSnapshot
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal


async def get_card_by_url(url: str, db: AsyncSession) -> TrackingItem | None:
    query = select(TrackingItem).where(TrackingItem.url == url)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_source_id(source_url: str, db: AsyncSession) -> int | None:
    query = select(Source.id).where(
    Source.url == source_url,
        Source.is_collected == True
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def user_watch_card_add(user_id: int, card_id: int, db: AsyncSession) -> None:
    new_watch = UsersTrackingItem(user_id=user_id, tracking_item_id=card_id)
    db.add(new_watch)
    await db.flush()


async def check_user_card_watch(user_id: int, card_id: int, db: AsyncSession) -> bool | None:
    query = select(
        exists().where(
            UsersTrackingItem.user_id == user_id,
            UsersTrackingItem.tracking_item_id == card_id
        )
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_card(url: str, name: str, is_in_stock: bool | None, source_id: int, db: AsyncSession) -> TrackingItem:
    new_card = TrackingItem(
        url=url,
        name=name,
        is_in_stock=is_in_stock,
        source_id=source_id
    )
    db.add(new_card)
    await db.flush()
    await db.refresh(new_card)
    return new_card


async def create_price_snapshot(item_id: int, price: Decimal | None, currency: str | None, db: AsyncSession) -> PriceSnapshot:
    new_price_snapshot = PriceSnapshot(
        tracking_item_id=item_id,
        price=price,
        currency=currency
    )
    db.add(new_price_snapshot)
    await db.flush()
    await db.refresh(new_price_snapshot)
    return new_price_snapshot
