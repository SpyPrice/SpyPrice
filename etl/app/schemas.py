from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class ItemRequest(BaseModel):
    user_id: int
    url: str
    source_id: int

class ItemResponse(BaseModel):
    user_id: int
    url: str
    name: str
    source_id: int
    is_in_stock: str | None
    price: Decimal
    currency: str
