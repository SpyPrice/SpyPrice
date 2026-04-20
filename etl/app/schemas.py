from pydantic import BaseModel
from decimal import Decimal


class ItemCreateWithPriceSnapshot(BaseModel):
    user_id: int
    url: str
    name: str
    source_id: int
    is_in_stock: bool | None = None
    price: Decimal
    currency: str


class AskNewItemParse(BaseModel):
    url: str
    user_id: int
    source_id: int
    callback_url: str


class ParseError(BaseModel):
    source_id: int
    url: str
    message: str
