from database import Base
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Boolean, Numeric, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import List
from decimal import Decimal


# Промежуточные таблицы
# для связи тегов и товаров (many-to-many)
tags_tracking_items = Table(
    'tags_tracking_items',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
    Column('tracking_item_id', Integer, ForeignKey('tracking_items.id'), primary_key=True)
)


# Таблицы(модели)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, comment='Уникальный идентификатор пользователя')
    login = Column(String, nullable=False, unique=True, comment='Логин пользователя')
    password = Column(String, nullable=False, comment='Хэш пароля')
    email = Column(String(127), nullable=False, unique=True, comment='Email пользователя')
    created_at = Column(DateTime, server_default=func.now(), comment='Дата создания')
    updated_at = Column(DateTime, onupdate=func.now(), comment='Дата последнего обновления')

    tracking_links = relationship(
        'UsersTrackingItem',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='selectin'
    )

    @property
    def tracking_items(self) -> List['TrackingItem']:
        return [link.tracking_item for link in self.tracking_links]


class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True, comment='Идентификатор источника')
    url = Column(Text, nullable=False, comment='Базовый URL источника')
    name = Column(String, nullable=False, comment='Название источника')
    is_collected = Column(Boolean, comment='Доступен ли ресурс для сбора данных')
    created_at = Column(DateTime, server_default=func.now(), comment='Дата создания')
    updated_at = Column(DateTime, onupdate=func.now(), comment='Дата последнего обновления')

    # Связь источник имеет товары
    tracking_items = relationship(
        'TrackingItem',
        back_populates='source',
        cascade='all, delete-orphan',
        lazy='selectin'
    )


class PriceSnapshot(Base):
    __tablename__ = 'price_snapshots'

    id = Column(Integer, primary_key=True, comment='Идентификатор снимка')
    tracking_item_id = Column(Integer, ForeignKey('tracking_items.id'), nullable=False, comment='ID товара')
    price = Column(Numeric(10, 2), comment='Цена в момент снимка')
    currency = Column(String(3), default='RUB', comment='Валюта цены')
    created_at = Column(DateTime, server_default=func.now(), comment='Время создания снимка')

    # снимок относится к товару
    tracking_item = relationship('TrackingItem', back_populates='price_snapshots')


# индекс для быстрого получения последней цены
Index(
    'ix_price_snapshots_item_created_desc',
    PriceSnapshot.tracking_item_id,
    PriceSnapshot.created_at.desc()
)


class TrackingItem(Base):
    __tablename__ = 'tracking_items'

    id = Column(Integer, primary_key=True, comment='Уникальный идентификатор товара')
    name = Column(String, comment='Название товара')
    url = Column(Text, nullable=False, comment='Ссылка на товар')
    is_in_stock = Column(Boolean, comment='Товар в наличии')

    source_id = Column(Integer, ForeignKey('sources.id'), comment='Ссылка на источник')

    created_at = Column(DateTime, server_default=func.now(), comment='Дата создания')
    updated_at = Column(DateTime, onupdate=func.now(), comment='Дата последнего обновления')

    # товар получен из источника
    source = relationship('Source', back_populates='tracking_items', lazy='selectin')

    # many-to-many теги
    tags = relationship('Tag', secondary=tags_tracking_items, back_populates='tracking_items', lazy='selectin')

    # связь с пользователями
    user_links = relationship(
        'UsersTrackingItem',
        back_populates='tracking_item',
        cascade='all, delete-orphan',
        lazy='selectin')

    # история цен
    price_snapshots = relationship(
        'PriceSnapshot',
        back_populates='tracking_item',
        cascade='all, delete-orphan',
        order_by='PriceSnapshot.created_at',
        lazy='selectin'
    )

    @property
    def last_price(self) -> Decimal | None:
        """Возвращает последнюю цену из загруженных в память снимков."""
        if self.price_snapshots:
            return self.price_snapshots[-1].price
        return None

    @property
    def users(self) -> List[User]:
        return [link.user for link in self.user_links]


class UsersTrackingItem(Base):
    __tablename__ = 'users_tracking_items'

    id = Column(Integer, primary_key=True, comment='Уникальный идентификатор связи')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='ID пользователя')
    tracking_item_id = Column(Integer, ForeignKey('tracking_items.id'), nullable=False, comment='ID товара')
    created_at = Column(DateTime, server_default=func.now(), comment='Дата добавления товара пользователем')
    updated_at = Column(DateTime, onupdate=func.now(), comment='Дата последнего обновления связи')

    # Связи для удобной навигации
    user = relationship('User', back_populates='tracking_links', lazy='selectin')
    tracking_item = relationship('TrackingItem', back_populates='user_links', lazy='selectin')


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True, comment='Название тега (уникальное)')
    description = Column(Text, comment='Описание тега')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # тег относится к товарам (many-to-many)
    tracking_items = relationship(
        'TrackingItem',
        secondary=tags_tracking_items,
        back_populates='tags',
        comment='Товары, отмеченные этим тегом',
        lazy='selectin'
    )
