from app.models import TrackingItem, UsersTrackingItem, Source, PriceSnapshot, Tag, tags_tracking_items
from sqlalchemy import Sequence, select, delete, update, exists, literal_column, union_all
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from datetime import datetime, timedelta


async def get_card_by_url(url: str, db: AsyncSession) -> TrackingItem | None:
    query = select(TrackingItem).where(TrackingItem.url == url)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_card_by_id(card_id: int, db: AsyncSession) -> TrackingItem | None:
    query = select(TrackingItem).where(TrackingItem.id == card_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


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


async def change_card_name_and_stock(item_id: int, name: str, is_in_stock: bool | None, db: AsyncSession):
    query = (
        update(TrackingItem)
        .where(TrackingItem.id == item_id)
        .values(name=name, is_in_stock=is_in_stock)
    )
    await db.execute(query)
    await db.flush()


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


async def get_all_card_ids(db: AsyncSession) -> Sequence[TrackingItem]:
    query = select(TrackingItem.id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_all_cards_id_source_url(db: AsyncSession):
    query = select(TrackingItem.id, TrackingItem.source_id, TrackingItem.url).order_by(TrackingItem.source_id)
    result = await db.execute(query)
    return result.all()


async def get_tags_for_user_item(user_id: int, card_id: int, db: AsyncSession) -> Sequence[tuple[int, str, str]]:
    query = (
        select(Tag.id, Tag.name, Tag.description)
        .join(Tag.tracking_items)
        .where(UsersTrackingItem.user_id == user_id,
               UsersTrackingItem.tracking_item_id == card_id
        )
    )
    result = await db.execute(query)
    return result.all()


async def get_all_user_tags(user_id: int, db: AsyncSession) -> Sequence[tuple[int, str, str]]:
    query = (
        select(Tag.id, Tag.name, Tag.description)
        .join(Tag.tracking_items)
        .where(UsersTrackingItem.user_id == user_id)
    )
    result = await db.execute(query)
    return result.all()


async def get_id_link_user_to_card(user_id: int, card_id: int, db: AsyncSession) -> int | None:
    query = (
        select(UsersTrackingItem.id)
        .where(UsersTrackingItem.user_id == user_id,
               UsersTrackingItem.tracking_item_id == card_id)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_user_tags(tag_names, db: AsyncSession) -> Sequence[int]:
    query = (
        pg_insert(Tag)
        .values(tag_names)
        .on_conflict_do_update(
            index_elements=[Tag.name],
            set_={Tag.name: Tag.name}
        )
        .returning(Tag.id)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def add_user_tag_to_item(tag_id: int, id_link_user_to_card: int, db: AsyncSession):
    query = (
        pg_insert(tags_tracking_items)
        .values(tag_id=tag_id, user_tracking_id=id_link_user_to_card)
        .on_conflict_do_nothing()
    )
    await db.execute(query)


async def delete_link_card_user(card_id: int, user_id: int, db: AsyncSession):
    query = (
        delete(UsersTrackingItem)
        .where(
            UsersTrackingItem.user_id == user_id,
            UsersTrackingItem.tracking_item_id == card_id
        )
    )
    await db.execute(query)


async def get_card_snapshots(card_id: int, db: AsyncSession) -> Sequence[Decimal, datetime]:
    query = (
        select(PriceSnapshot.price, PriceSnapshot.created_at)
        .where(PriceSnapshot.tracking_item_id == card_id)
        .order_by(PriceSnapshot.created_at.asc())
    )
    result = await db.execute(query)
    return result.all()


async def get_card_last_and_week_snapshot(card_id: int, db: AsyncSession):
    week_ago = datetime.now() - timedelta(days=7)
    month_ago = datetime.now() - timedelta(days=30)

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

    very_old_query = (
        select(
            PriceSnapshot.price,
            PriceSnapshot.created_at,
            literal_column("'very_old'").label('type')
        )
        .where(PriceSnapshot.tracking_item_id == card_id, PriceSnapshot.created_at <= month_ago)
        .order_by(PriceSnapshot.created_at.desc())
        .limit(1)
    )

    combined = union_all(last_query, old_query, very_old_query).subquery()
    result = await db.execute(select(combined))
    rows = result.all()

    data = {'last': None, 'old': None, 'very_old': None}
    for row in rows:
        data[row.type] = row

    return data
