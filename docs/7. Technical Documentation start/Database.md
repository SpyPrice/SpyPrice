# База данных (предварительная ER-схема)

Цель: единое понимание модели домена между `Database.md` ↔ `API.md` ↔ `Parser Architecture.md`.

СУБД: **PostgreSQL**.

## Сущности и поля

### `User`
- `id` (UUID, PK)
- `email` (varchar, unique, not null)
- `hashed_password` (varchar, not null)
- `registered_at` (timestamptz, not null)
- `is_deleted` (boolean, default false)

### `Source`
- `id` (UUID, PK)
- `name` (varchar, not null)
- `base_url` (varchar, not null)
- `parser_type` (varchar, not null) — тип адаптера (например `ozon_html`)
- `created_at` (timestamptz, not null)

### `Product`
- `id` (UUID, PK)
- `user_id` (UUID, FK → `User.id`, not null)
- `source_id` (UUID, FK → `Source.id`, not null)
- `url` (varchar, not null)
- `name` (varchar, not null)
- `tags` (jsonb, опционально) или `varchar[]`
- `created_at` (timestamptz, not null)
- `updated_at` (timestamptz, not null)
- `is_deleted` (boolean, default false)

### `PriceSnapshot`
Срез цены “в момент времени”.
- `id` (UUID, PK)
- `product_id` (UUID, FK → `Product.id`, not null)
- `price` (DECIMAL(12,2), not null)
- `currency` (char(3), not null) — например `RUB`
- `fetched_at` (timestamptz, not null)
- `status` (enum: `success`, `error`, not null)
- `error_message` (text, null) — если status=`error`
- `raw_data` (jsonb, null) — опционально (для дебага адаптера)

Дедупликация (на MVP):
- вариант 1: хранить все снимки, даже если одинаковые цены
- вариант 2: предотвращать дубли через уникальность `(product_id, fetched_at)` (или округление fetched_at)

Рекомендация: вариант 2, чтобы ETL мог безопасно ретраить.

### `AlertRule` (опционально для MVP)
- `id` (UUID, PK)
- `user_id` (UUID, FK → `User.id`, not null)
- `product_id` (UUID, FK → `Product.id`, not null)
- `threshold_type` (enum: `absolute`, `percent`, not null)
- `threshold_value` (DECIMAL(12,2), not null)
- `is_active` (boolean, default true)
- `created_at` (timestamptz, not null)

### `AlertEvent` (опционально для MVP)
- `id` (UUID, PK)
- `rule_id` (UUID, FK → `AlertRule.id`, not null)
- `triggered_at` (timestamptz, not null)
- `price_at_trigger` (DECIMAL(12,2), not null)

## Связи (каркас)
- `User (1)` → `Product (many)` через `Product.user_id`
- `Source (1)` → `Product (many)` через `Product.source_id`
- `Product (1)` → `PriceSnapshot (many)` через `PriceSnapshot.product_id`
- `AlertRule (1)` → `AlertEvent (many)` через `AlertEvent.rule_id`

## Индексы (для быстрых запросов MVP)
- `PriceSnapshot`: индекс по `(product_id, fetched_at desc)`
- `Product`: индекс по `(user_id, created_at desc)`
- `AlertEvent`: индекс по `(rule_id, triggered_at desc)`

## Миграции
- Используем **Alembic**.
- Правило нейминга миграций: “описательно” + timestamp (по принятому в репозитории шаблону).
- Любые изменения в полях/типах (особенно `PriceSnapshot.price`) должны сопровождаться обновлением `API.md`.

