from typing import Any

from app.models import TrackingItem, UsersTrackingItem, Source, PriceSnapshot
from sqlalchemy import Sequence, select, exists, literal_column, union_all, Row
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from datetime import datetime, timedelta


async def get_card_by_url(url: str, db: AsyncSession) -> TrackingItem | None:
    query = select(TrackingItem).where(TrackingItem.url == url)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_card_by_id(card_id: int, db: AsyncSession) -> TrackingItem:
    query = select(TrackingItem).where(TrackingItem.id == card_id)
    result = await db.execute(query)
    return result.scalar_one()


async def get_source_id(source_url: str, db: AsyncSession) -> int | None:
    query = select(Source.id).where(
    Source.url == source_url,
        Source.is_collected == True
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_source_by_id(source_id: int, db: AsyncSession) -> Source:
    query = select(Source).where(
        Source.id == source_id
    )
    result = await db.execute(query)
    return result.scalar_one()


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


async def get_user_cards(user_id: int, db: AsyncSession) -> Sequence[UsersTrackingItem]:
    query = select(UsersTrackingItem).where(UsersTrackingItem.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_card_snapshots(card_id: int, db: AsyncSession) -> Sequence[Decimal, datetime]:
    query = (
        select(PriceSnapshot.price, PriceSnapshot.currency, PriceSnapshot.created_at)
        .where(PriceSnapshot.tracking_item_id == card_id)
        .order_by(PriceSnapshot.created_at.asc())
    )
    result = await db.execute(query)
    return result.all()

async def get_card_last_and_week_snapshot(card_id: int, db: AsyncSession):
    week_ago = datetime.now() - timedelta(days=7)

    last_query = (
        select(
            PriceSnapshot.price,
            PriceSnapshot.created_at,
            literal_column("'last'").label('type')
        )
        .where(PriceSnapshot.tracking_item_id == card_id)
        .order_by(PriceSnapshot.created_at.desc())
        .limit(1)
    )

    old_query = (
        select(
            PriceSnapshot.price,
            PriceSnapshot.created_at,
            literal_column("'old'").label('type')
        )
        .where(PriceSnapshot.tracking_item_id == card_id, PriceSnapshot.created_at <= week_ago)
        .order_by(PriceSnapshot.created_at.desc())
        .limit(1)
    )

    combined = union_all(last_query, old_query).subquery()
    result = await db.execute(select(combined))
    rows = result.all()

    data = {'last': None, 'old': None}
    for row in rows:
        data[row.type] = row

    return data
