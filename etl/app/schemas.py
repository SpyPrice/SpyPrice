from pydantic import BaseModel
from decimal import Decimal


class MyDataModels(BaseModel):
    pass


class AskNewItemParse(MyDataModels):
    url: str
    user_id: int
    source_id: int
    callback_url: str


class AskExistsItemParse(MyDataModels):
    item_id: int
    url: str
    source_id: int
    callback_url: str


class ParseError(MyDataModels):
    source_id: int
    url: str
    message: str


class ParseResult(MyDataModels):
    name: str
    price: Decimal
    currency: str


class ItemCreateWithPriceSnapshot(MyDataModels):
    user_id: int
    url: str
    name: str
    source_id: int
    is_in_stock: bool | None = None
    price: Decimal
    currency: str


class PriceSnapshotCreate(MyDataModels):
    tracking_item_id: int
    price: Decimal
    currency: str
