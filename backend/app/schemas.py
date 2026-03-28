from pydantic import BaseModel, Field, ConfigDict
from pydantic import EmailStr, HttpUrl
from decimal import Decimal
from datetime import datetime


class MyDataModels(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TimestampedModels(MyDataModels):
    created_at: datetime
    updated_at: datetime | None = None


class UserCreate(MyDataModels):
    """Запрос создания пользователя"""
    login: str = Field(..., min_length=5, max_length=127)
    password: str = Field(..., min_length=8, max_length=71)
    email: EmailStr = Field(..., min_length=5, max_length=127)


class UserRead(TimestampedModels):
    id: int
    login: str
    email: EmailStr


class TagCreate(MyDataModels):
    name: str = Field(..., min_length=2, max_length=60)
    description: str | None = Field(default=None, min_length=2, max_length=127)


class TagRead(TimestampedModels):
    id: int
    name: str
    description: str | None


class PriceSnapshotRead(MyDataModels):
    id: int
    tracking_item_id: int
    price: Decimal
    currency: str
    created_at: datetime


class ItemCreateRequest(MyDataModels):
    """Запрос но добавление нового отслеживаемого предмета от пользователя"""
    # Имя ресурса можно получить во время обработки ссылки.
    # source_name: str = Field(..., min_length=1, max_length=255)
    source_url: HttpUrl = Field(..., max_length=511)


class ItemUpdateRequest(MyDataModels):
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
