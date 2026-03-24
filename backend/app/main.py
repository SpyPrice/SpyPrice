from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, SessionLocal, engine, get_db
from app.deps import get_current_user, validate_etl_key
from app.models import PriceSnapshot, Product, Source, User
from app.schemas import (
    AuthResponse,
    LoginResponse,
    MetricsResponse,
    OkResponse,
    ProductCreate,
    ProductOut,
    ProductPatch,
    ProductsResponse,
    RegisterRequest,
    SnapshotHistoryResponse,
    SnapshotIngestIn,
    SnapshotOut,
    SourceOut,
    SourcesResponse,
    UserMeResponse,
)
from app.security import create_access_token, hash_password, verify_password

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_sources(db)
    finally:
        db.close()


def seed_sources(db: Session) -> None:
    defaults = [
        ("DNS", "https://www.dns-shop.ru", "dns_html"),
        ("Ozon", "https://www.ozon.ru", "ozon_html"),
    ]
    for name, base_url, parser_type in defaults:
        exists = db.query(Source).filter(Source.parser_type == parser_type).first()
        if not exists:
            db.add(Source(name=name, base_url=base_url, parser_type=parser_type))
    db.commit()


@app.post(f"{settings.api_prefix}/auth/register", response_model=AuthResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> AuthResponse:
    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=409, detail="Email already exists")
    user = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return AuthResponse(user_id=user.id, email=user.email)


@app.post(f"{settings.api_prefix}/auth/login", response_model=LoginResponse)
def login(payload: RegisterRequest, db: Session = Depends(get_db)) -> LoginResponse:
    user = db.query(User).filter(User.email == payload.email, User.is_deleted.is_(False)).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token, ttl = create_access_token(str(user.id))
    return LoginResponse(access_token=token, expires_in=ttl)


@app.get(f"{settings.api_prefix}/auth/me", response_model=UserMeResponse)
def me(user: User = Depends(get_current_user)) -> UserMeResponse:
    return UserMeResponse(user_id=user.id, email=user.email, registered_at=user.registered_at)


@app.get(f"{settings.api_prefix}/sources", response_model=SourcesResponse)
def sources(db: Session = Depends(get_db)) -> SourcesResponse:
    rows = db.query(Source).order_by(Source.name.asc()).all()
    return SourcesResponse(items=[SourceOut(id=s.id, name=s.name, base_url=s.base_url, parser_type=s.parser_type) for s in rows])


@app.get(f"{settings.api_prefix}/products", response_model=ProductsResponse)
def list_products(
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    tags: list[str] = Query(default=[]),
    source_id: UUID | None = Query(default=None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProductsResponse:
    query = db.query(Product).filter(Product.user_id == user.id, Product.is_deleted.is_(False))
    if source_id:
        query = query.filter(Product.source_id == source_id)
    if tags:
        query = query.filter(Product.tags.contains(tags))

    total = query.count()
    rows = query.order_by(Product.created_at.desc()).offset(offset).limit(limit).all()
    items = []
    for p in rows:
        s = p.source
        items.append(
            ProductOut(
                id=p.id,
                url=p.url,
                name=p.name,
                source=SourceOut(id=s.id, name=s.name, base_url=s.base_url, parser_type=s.parser_type),
                tags=p.tags or [],
            )
        )
    return ProductsResponse(items=items, total=total)


@app.post(f"{settings.api_prefix}/products", response_model=ProductOut, status_code=201)
def create_product(payload: ProductCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ProductOut:
    source = db.query(Source).filter(Source.id == payload.source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    product = Product(user_id=user.id, source_id=payload.source_id, url=str(payload.url), name=payload.name, tags=payload.tags)
    db.add(product)
    db.commit()
    db.refresh(product)
    return ProductOut(
        id=product.id,
        url=product.url,
        name=product.name,
        source=SourceOut(id=source.id, name=source.name, base_url=source.base_url, parser_type=source.parser_type),
        tags=product.tags or [],
    )


@app.patch(f"{settings.api_prefix}/products/{{product_id}}", response_model=ProductOut)
def patch_product(product_id: UUID, payload: ProductPatch, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ProductOut:
    product = db.query(Product).filter(Product.id == product_id, Product.user_id == user.id, Product.is_deleted.is_(False)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if payload.name is not None:
        product.name = payload.name
    if payload.tags is not None:
        product.tags = payload.tags
    db.commit()
    db.refresh(product)
    source = product.source
    return ProductOut(
        id=product.id,
        url=product.url,
        name=product.name,
        source=SourceOut(id=source.id, name=source.name, base_url=source.base_url, parser_type=source.parser_type),
        tags=product.tags or [],
    )


@app.delete(f"{settings.api_prefix}/products/{{product_id}}", response_model=OkResponse)
def delete_product(product_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> OkResponse:
    product = db.query(Product).filter(Product.id == product_id, Product.user_id == user.id, Product.is_deleted.is_(False)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.is_deleted = True
    db.commit()
    return OkResponse(ok=True)


@app.get(f"{settings.api_prefix}/products/{{product_id}}/history", response_model=SnapshotHistoryResponse)
def product_history(
    product_id: UUID,
    from_: datetime | None = Query(default=None, alias="from"),
    to: datetime | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SnapshotHistoryResponse:
    product = db.query(Product).filter(Product.id == product_id, Product.user_id == user.id, Product.is_deleted.is_(False)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    query = db.query(PriceSnapshot).filter(PriceSnapshot.product_id == product_id)
    if from_:
        query = query.filter(PriceSnapshot.fetched_at >= from_)
    if to:
        query = query.filter(PriceSnapshot.fetched_at <= to)
    rows = query.order_by(PriceSnapshot.fetched_at.desc()).offset(offset).limit(limit).all()
    return SnapshotHistoryResponse(
        items=[
            SnapshotOut(
                id=r.id,
                price=str(r.price),
                currency=r.currency,
                fetched_at=r.fetched_at,
                status=r.status,
                error_message=r.error_message,
                availability=r.availability,
            )
            for r in rows
        ]
    )


@app.get(f"{settings.api_prefix}/products/{{product_id}}/metrics", response_model=MetricsResponse)
def product_metrics(
    product_id: UUID,
    from_: datetime | None = Query(default=None, alias="from"),
    to: datetime | None = Query(default=None),
    preset: str | None = Query(default=None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MetricsResponse:
    product = db.query(Product).filter(Product.id == product_id, Product.user_id == user.id, Product.is_deleted.is_(False)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not from_ and not to and preset in ("7d", "30d"):
        days = 7 if preset == "7d" else 30
        to = datetime.now(timezone.utc)
        from_ = to - timedelta(days=days)

    filters = [PriceSnapshot.product_id == product_id, PriceSnapshot.status == "success"]
    if from_:
        filters.append(PriceSnapshot.fetched_at >= from_)
    if to:
        filters.append(PriceSnapshot.fetched_at <= to)

    rows = db.query(PriceSnapshot).filter(and_(*filters)).order_by(PriceSnapshot.fetched_at.asc()).all()
    if not rows:
        zero = "0.00"
        return MetricsResponse(currency="RUB", min=zero, max=zero, avg=zero, delta=zero, delta_percent=zero, period={"from": from_, "to": to})

    prices = [Decimal(str(r.price)) for r in rows]
    min_v = min(prices)
    max_v = max(prices)
    avg_v = sum(prices) / Decimal(len(prices))
    delta = prices[-1] - prices[0]
    delta_percent = Decimal("0.00")
    if prices[0] != 0:
        delta_percent = (delta / prices[0]) * Decimal("100")
    return MetricsResponse(
        currency=rows[-1].currency,
        min=f"{min_v:.2f}",
        max=f"{max_v:.2f}",
        avg=f"{avg_v:.2f}",
        delta=f"{delta:.2f}",
        delta_percent=f"{delta_percent:.2f}",
        period={"from": from_ or rows[0].fetched_at, "to": to or rows[-1].fetched_at},
    )


@app.post(f"{settings.api_prefix}/price-snapshots/internal", response_model=OkResponse, dependencies=[Depends(validate_etl_key)])
def ingest_snapshot(payload: SnapshotIngestIn, db: Session = Depends(get_db)) -> OkResponse:
    product = db.query(Product).filter(Product.id == payload.product_id, Product.is_deleted.is_(False)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    snapshot = PriceSnapshot(
        product_id=payload.product_id,
        price=payload.price,
        currency=payload.currency,
        fetched_at=payload.fetched_at,
        status=payload.status,
        error_message=payload.error_message,
        availability=payload.availability or "unknown",
        raw_data=payload.raw_data,
    )
    db.add(snapshot)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return OkResponse(ok=True)
    return OkResponse(ok=True)
