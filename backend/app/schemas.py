from pydantic import BaseModel, Field, ConfigDict
from pydantic import EmailStr, HttpUrl
from typing import Literal
from decimal import Decimal
from datetime import datetime


class MyDataModels(BaseModel):
    pass


class TimestampedModels(MyDataModels):
    created_at: datetime
    updated_at: datetime | None = None


class UserCreate(MyDataModels):
    """Запрос создания пользователя"""
    name: str = Field(..., min_length=3, max_length=127)
    password: str = Field(..., min_length=8, max_length=71)
    email: EmailStr


class UserRead(TimestampedModels):
    id: int
    name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class Token(MyDataModels):
    access_token: str
    token_type: str = "bearer"


class TokenWithUser(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class TagCreate(MyDataModels):
    name: str = Field(..., min_length=2, max_length=60)
    description: str | None = Field(default=None, min_length=2, max_length=127)


class TagRead(TimestampedModels):
    id: int
    name: str
    description: str | None
    model_config = ConfigDict(from_attributes=True)


class ItemCreate(MyDataModels):
    """Запрос но добавление нового отслеживаемого предмета от пользователя"""
    # Имя ресурса можно получить во время обработки ссылки.
    # source_name: str = Field(..., min_length=1, max_length=255)
    source_url: HttpUrl = Field(..., max_length=511)


class ItemUpdate(MyDataModels):
    name: str | None = None
    url: str | None = None
    is_in_stock: bool | None = None


class ItemRead(TimestampedModels):
    id: int
    name: str
    url: str
    is_in_stock: bool | None = None
    source_id: int
    source_name: str
    tags: list[TagRead] = Field(default_factory=list)
    """Последняя цена на товар"""
    last_price: Decimal | None = None
    model_config = ConfigDict(from_attributes=True)


class WatchResponse(MyDataModels):
    status: Literal['success', 'exists', 'pending', 'error']
    message: str


class PriceSnapshotCreate(MyDataModels):
    tracking_item_id: int
    price: Decimal
    currency: str
    created_at: datetime


class PriceSnapshotRead(MyDataModels):
    id: int
    tracking_item_id: int
    price: Decimal
    currency: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class SourceRead(TimestampedModels):
    id: int
    url: str
    name: str
    is_collected: bool
    model_config = ConfigDict(from_attributes=True)


class ItemCreateWithPriceSnapshot(MyDataModels):
    user_id: int
    url: str
    name: str
    source_id: int
    is_in_stock: str | None = None
    price: Decimal
    currency: str
