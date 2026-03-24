# Контракты данных (API ↔ UI ↔ ETL)

Зачем: чтобы изменения в `API.md` и модели `Database.md` не приводили к “тихим” рассинхронам на фронтенде и в ETL.

## Правила синхронизации
1. Все формы запросов/ответов (DTO) описываются в `API.md`.
2. Для фронтенда (Егор) создаётся отражение DTO в виде `Frontend types`:
   - либо прямо в `API.md` (небольшими блоками),
   - либо отдельным блоком в этом файле.
3. Для ETL (Эдик) ключевой контракт — это “выход” адаптера:
   - структура `ExtractionResult` (см. `Parser Architecture.md`)
   - и формат POST `/api/v1/price-snapshots/internal` (см. `API.md`).

## Минимальный набор типов (MVP)

### Product
```json
{
  "id": "uuid",
  "url": "string",
  "name": "string",
  "source": { "id": "uuid", "name": "string" },
  "tags": ["string"]
}
```

### PriceSnapshot
```json
{
  "id": "uuid",
  "product_id": "uuid",
  "price": "string(decimal)",
  "currency": "RUB",
  "fetched_at": "ISO-8601",
  "status": "success|error",
  "error_message": "string|null",
  "availability": "in_stock|out_of_stock|unknown"
}
```

Для внутреннего POST `/api/v1/price-snapshots/internal` поле `availability` опционально; при отсутствии трактуем как `unknown`.

## Про порядок обновлений
Если меняется:
- форма `POST /price-snapshots/internal` (ETL),
- поля `PriceSnapshot` (БД/ответы),
- формат `metrics`/`history` (фронт),

то в PR/коммите делайте короткую заметку в соответствующем разделе этого файла:
- `Дата`
- `Что изменили`
- `Куда это затронет` (API / ETL / UI)

