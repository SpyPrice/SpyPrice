from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, HttpUrl


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: dict | None = None


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class AuthResponse(BaseModel):
    user_id: UUID
    email: EmailStr


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserMeResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    registered_at: datetime


class SourceOut(BaseModel):
    id: UUID
    name: str
    base_url: str
    parser_type: str


class SourcesResponse(BaseModel):
    items: list[SourceOut]


class ProductCreate(BaseModel):
    url: HttpUrl
    name: str = Field(min_length=1, max_length=255)
    source_id: UUID
    tags: list[str] = []


class ProductPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    tags: list[str] | None = None


class ProductOut(BaseModel):
    id: UUID
    url: str
    name: str
    source: SourceOut
    tags: list[str]


class ProductsResponse(BaseModel):
    items: list[ProductOut]
    total: int


class SnapshotOut(BaseModel):
    id: UUID
    price: str
    currency: str
    fetched_at: datetime
    status: str
    error_message: str | None
    availability: str


class SnapshotHistoryResponse(BaseModel):
    items: list[SnapshotOut]


class MetricsResponse(BaseModel):
    currency: str
    min: str
    max: str
    avg: str
    delta: str
    delta_percent: str
    period: dict


class SnapshotIngestIn(BaseModel):
    product_id: UUID
    price: str = "0"
    currency: str = "RUB"
    fetched_at: datetime
    status: str = "success"
    error_message: str | None = None
    availability: str | None = None
    raw_data: dict | None = None


class OkResponse(BaseModel):
    ok: bool = True
