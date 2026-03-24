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
{ "email": "user@example.com", "password": "plain_password" }
```

**Response**
```json
{ "user_id": "uuid", "email": "user@example.com" }
```

### POST `/api/v1/auth/login`
Войти и получить JWT.

**Request**
```json
{ "email": "user@example.com", "password": "plain_password" }
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
{ "user_id": "uuid", "email": "user@example.com", "registered_at": "2026-03-20T10:10:10Z" }
```

## Sources (магазины/источники)

### GET `/api/v1/sources`
Список источников, которые поддерживаются системой.

**Response**
```json
{
  "items": [
    { "id": "uuid", "name": "Ozon", "base_url": "https://...", "parser_type": "ozon_html" }
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
- `source_id` (опционально, UUID — фильтр по магазину/источнику; соответствует ТЗ «фильтрация по магазинам»)

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

### PATCH `/api/v1/products/{product_id}`
Частичное обновление карточки товара (имя, теги и т.п.).

**Request** (все поля опциональны; передаются только изменяемые)
```json
{
  "name": "Новое имя",
  "tags": ["тег1", "тег2"]
}
```

**Response**
```json
{ "id": "uuid", "url": "https://...", "name": "...", "tags": ["..."] }
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
      "error_message": null,
      "availability": "unknown"
    }
  ]
}
```

Поле **`availability`** (согласование с ТЗ «статус доступности»): например `in_stock` | `out_of_stock` | `unknown`. Если источник не отдаёт наличие — всегда `unknown`.

### GET `/api/v1/products/{product_id}/metrics`
Агрегированные метрики за период.

**Query** (один из вариантов)
- **Вариант A**: `from` / `to` (ISO-8601) — произвольный интервал.
- **Вариант B**: `preset` — преднастроенные окна из ТЗ: `7d` | `30d` (удобно для «изменение за 7/30 дней» без выбора дат на фронте).

Если заданы и `preset`, и `from`/`to`, приоритет нужно зафиксировать в реализации (рекомендация: `preset` игнорируется, если заданы `from`/`to`).

**Response**
```json
{
  "currency": "RUB",
  "min": "1800.00",
  "max": "2400.00",
  "avg": "2050.50",
  "delta": "200.00",
  "delta_percent": "11.11",
  "period": { "from": "2026-03-01T00:00:00Z", "to": "2026-03-20T23:59:59Z" }
}
```

## Аналитика и экспорт (MVP+: Спринт 4 / к финалу)

Ниже — целевой контракт под требования ТЗ («топ падений/роста», экспорт CSV). До реализации помечать в OpenAPI как **planned** или выносить за флагом, чтобы не ломать фронт.

### GET `/api/v1/analytics/top-movers`
Сводка по товарам текущего пользователя: наибольшие падения и рост цены за период.

**Query**
- `from` / `to` (ISO-8601) **или** `preset`: `7d` | `30d`
- `limit` (default 10) — сколько позиций в каждой категории (рост/падение)

**Response** (пример)
```json
{
  "period": { "from": "...", "to": "..." },
  "top_increases": [
    { "product_id": "uuid", "name": "...", "delta_percent": "15.00" }
  ],
  "top_decreases": [
    { "product_id": "uuid", "name": "...", "delta_percent": "-22.50" }
  ]
}
```

### GET `/api/v1/export/products.csv`
Экспорт списка отслеживаемых товаров пользователя (опционально для MVP).

**Query**: те же фильтры, что у `GET /products` (`tags`, `source_id`).

**Response**: `Content-Type: text/csv`, файл со столбцами согласованного формата (задокументировать в репозитории при появлении реализации).

### GET `/api/v1/products/{product_id}/history.csv`
Экспорт истории цен по одному товару (опционально для MVP).

**Query**: `from`, `to` — как у JSON-истории.

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
  "availability": "in_stock",
  "raw_data": { "provider": "...", "html_snippet": "..." }
}
```

Поле **`availability`** опционально; если не передано — в БД сохраняется как `unknown` (или эквивалент).

**Response**
```json
{ "ok": true }
```

## Что нужно согласовать между слоями
- Модель статусов `PriceSnapshot.status`: какие значения разрешены (`success/error` в MVP).
- Допустимые значения `availability` и поведение при отсутствии в ответе источника.
- Валюта и формат денег: хранение в `DECIMAL`, отдача как строка (чтобы не терять точность).
- Идемпотентность ETL: как избежать дублей при повторных запусках (обычно уникальность по `(product_id, fetched_at)` или дедупликация на уровне ETL).

