from .database import Base
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Boolean, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


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
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, comment='Уникальный идентификатор пользователя')
    login = Column(String, nullable=False, unique=True, comment='Логин пользователя')
    password = Column(String, nullable=False, comment='Хэш пароля')
    email = Column(String, nullable=False, unique=True, comment='Email пользователя')
    created_at = Column(DateTime, server_default=func.now(), comment='Дата создания')
    updated_at = Column(DateTime, onupdate=func.now(), comment='Дата последнего обновления')

    # Связь с промежуточной таблицей (через класс)
    tracking_links = relationship('UsersTrackingItem', back_populates='user', cascade='all, delete-orphan')

    # Это теставая штука, но должна быть удобной(доступ к товарам напрямую)
    @property
    def tracking_items(self):
        return [link.tracking_item for link in self.tracking_links]


class Source(Base):
    __tablename__ = 'Sources'

    id = Column(Integer, primary_key=True, comment='Идентификатор источника')
    url = Column(String, comment='Базовый URL источника')
    name = Column(String, nullable=False, comment='Название источника')
    is_collected = Column(Boolean)
    created_at = Column(DateTime, server_default=func.now(), comment='Дата создания')
    updated_at = Column(DateTime, onupdate=func.now(), comment='Дата последнего обновления')

    # Связь источник имеет товары
    tracking_items = relationship('TrackingItem', back_populates='source', cascade='all, delete-orphan')


class TrackingItem(Base):
    __tablename__ = 'Tracking_items'

    id = Column(Integer, primary_key=True, comment='Уникальный идентификатор товара')
    name = Column(String, comment='Название товара')
    url = Column(String, nullable=False, comment='Ссылка на товар')
    is_in_stock = Column(Boolean, comment='Товар в наличии')
    source_id = Column(Integer, ForeignKey('sources.id'), comment='Ссылка на источник')
    created_at = Column(DateTime, server_default=func.now(), comment='Дата создания')
    updated_at = Column(DateTime, onupdate=func.now(), comment='Дата последнего обновления')

    # товар получен из источника
    source = relationship('Source', back_populates='tracking_items')

    # товар имеет снимки цен
    price_snapshots = relationship(
        'PriceSnapshot',
        back_populates='tracking_item',
        cascade='all, delete-orphan' # это если нужно удалить товар, чтобы удалилось все остально с ним связанное
    )

    # товар имеет теги (many-to-many)
    tags = relationship(
        'Tag',
        secondary=tags_tracking_items,
        back_populates='tracking_items',
        comment='Теги, присвоенные товару'
    )

    # Удобный доступ к пользователям напрямую
    @property
    def users(self):
        return [link.user for link in self.user_links]


class PriceSnapshot(Base):
    __tablename__ = 'Price_snapshots'

    id = Column(Integer, primary_key=True, comment='Идентификатор снимка')
    tracking_item_id = Column(Integer, ForeignKey('tracking_items.id'), nullable=False, comment='Ссылка на товар')
    price = Column(Numeric(10, 2), comment='Цена в момент снимка')
    currency = Column(String, default='RUB', comment='Валюта цены')
    created_at = Column(DateTime, server_default=func.now(), comment='Время создания снимка')

    # снимок относится к товару
    tracking_item = relationship('TrackingItem', back_populates='price_snapshots')


class UsersTrackingItem(Base):
    __tablename__ = 'Users_tracking_items'

    id = Column(Integer, primary_key=True, comment='Уникальный идентификатор связи')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='ID пользователя')
    tracking_item_id = Column(Integer, ForeignKey('tracking_items.id'), nullable=False, comment='ID товара')
    created_at = Column(DateTime, server_default=func.now(), comment='Дата добавления товара пользователем')
    updated_at = Column(DateTime, onupdate=func.now(), comment='Дата последнего обновления связи')

    # Связи для удобной навигации
    user = relationship('User', back_populates='tracking_links')
    tracking_item = relationship('TrackingItem', back_populates='user_links')


class Tag(Base):
    __tablename__ = 'Tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True, comment='Название тега (уникальное)')
    description = Column(Text, comment='Описание тега')
    created_at = Column(DateTime, server_default=func.now(), comment='Дата создания тега')
    updated_at = Column(DateTime, onupdate=func.now(), comment='Дата последнего обновления')

    # тег относится к товарам (many-to-many)
    tracking_items = relationship(
        'TrackingItem',
        secondary=tags_tracking_items,
        back_populates='tags',
        comment='Товары, отмеченные этим тегом'
    )