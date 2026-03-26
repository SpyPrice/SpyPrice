from pydantic import BaseModel, EmailStr, Field, ConfigDict
from decimal import Decimal
from datetime import datetime


# Модель для создания пользователя
class UserCreate(BaseModel):
    login: str = Field(..., min_length=5, max_length=127)
    password: str = Field(..., min_length=8, max_length=71)
    email: EmailStr = Field(..., min_length=5, max_length=127)


class UserRead(BaseModel):
    login: str = Field(..., min_length=5, max_length=127)
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



class PriceSnapshot(BaseModel):
    price: Decimal



class Item(BaseModel):
    pass