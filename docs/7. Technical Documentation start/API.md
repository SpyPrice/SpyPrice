# API (контракты сервиса)

Стек: **FastAPI** → автоматическая документация на `/docs` (Swagger UI).

## Базовый формат
- Базовый префикс: `/api/v1`
- Формат: JSON
- Аутентификация: `Authorization: Bearer <access_token>` (JWT)
- Ошибки: единый формат ответа (см. `ErrorResponse`)

## Ошибки (единый формат)
```json
{
  "code": "string",
  "message": "человекочитаемое сообщение",
  "details": {
    "field": "validation error (опционально)"
  }
}
```

Пример `code`:
- `unauthorized`
- `forbidden`
- `not_found`
- `validation_error`
- `internal_error`

## Auth

### POST `/api/v1/auth/register`
Зарегистрировать пользователя.

**Request**
```json
{
	"email": "user@example.com",
	"password": "plain_password"
}
```

**Response**
```json
{
	"user_id": "uuid",
	"email": "user@example.com"
}
```

### POST `/api/v1/auth/login`
Войти и получить JWT.

**Request**
```json
{
	"email": "user@example.com",
	"password": "plain_password" 
}
```

**Response**
```json
{
  "access_token": "jwt_token",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### GET `/api/v1/auth/me`
Получить текущего пользователя.

**Response**
```json
{
	"user_id": "uuid",
	"email": "user@example.com",
	"registered_at": "2026-03-20T10:10:10Z"
}
```

## Sources (магазины/источники)

### GET `/api/v1/sources`
Список источников, которые поддерживаются системой.

**Response**
```json
{
  "items": [
    {
	    "id": "uuid",
	    "name": "Ozon",
	    "base_url": "https://...",
	    "parser_type": "ozon_html"
	}
  ]
}
```

## Products (товары)

### GET `/api/v1/products`
Список товаров текущего пользователя.

**Query**
- `limit` (default 20)
- `offset` (default 0)
- `tags` (опционально, повторяемый параметр)

**Response**
```json
{
  "items": [
    {
      "id": "uuid",
      "url": "https://...",
      "name": "Название товара",
      "source": { "id": "uuid", "name": "Ozon" },
      "tags": ["..."]
    }
  ],
  "total": 123
}
```

### POST `/api/v1/products`
Добавить товар по URL.

**Request**
```json
{
  "url": "https://...",
  "name": "Опционально. Если пусто — берём из страницы/ETL (на будущие спринты).",
  "source_id": "uuid",
  "tags": ["..."]
}
```

**Response**
```json
{ "id": "uuid", "url": "https://...", "name": "..." }
```

### DELETE `/api/v1/products/{product_id}`
Удалить (в MVP допускается soft-delete по полю `is_deleted`).

**Response**
```json
{ "ok": true }
```

## Price history & metrics

### GET `/api/v1/products/{product_id}/history`
История `PriceSnapshot` (таблица/лог).

**Query**
- `from` (ISO-8601, опционально)
- `to` (ISO-8601, опционально)
- `limit` (default 200)
- `offset` (default 0)

**Response**
```json
{
  "items": [
    {
      "id": "uuid",
      "price": "1999.99",
      "currency": "RUB",
      "fetched_at": "2026-03-20T10:10:10Z",
      "status": "success",
      "error_message": null
    }
  ]
}
```

### GET `/api/v1/products/{product_id}/metrics`
Агрегированные метрики за период.

**Query**
- `from` / `to` (ISO-8601)

**Response**
```json
{
  "currency": "RUB",
  "min": "1800.00",
  "max": "2400.00",
  "avg": "2050.50",
  "delta": "200.00",
  "delta_percent": "11.11"
}
```

## Internal: прием PriceSnapshot от ETL
Этот endpoint нужен, если ETL сохраняет данные “через backend” (рекомендуется для консистентности).

### POST `/api/v1/price-snapshots/internal`
**Security (MVP-вариант)**
- например, отдельный `ETL_API_KEY` в заголовке:
  - `X-ETL-API-Key: <secret>`

**Request**
```json
{
  "product_id": "uuid",
  "price": "1999.99",
  "currency": "RUB",
  "fetched_at": "2026-03-20T10:10:10Z",
  "status": "success",
  "error_message": null,
  "raw_data": { "provider": "...", "html_snippet": "..." }
}
```

**Response**
```json
{ "ok": true }
```

## Что нужно согласовать между слоями
- Модель статусов `PriceSnapshot.status`: какие значения разрешены (`success/error` в MVP).
- Валюта и формат денег: хранение в `DECIMAL`, отдача как строка (чтобы не терять точность).
- Идемпотентность ETL: как избежать дублей при повторных запусках (обычно уникальность по `(product_id, fetched_at)` или дедупликация на уровне ETL).

