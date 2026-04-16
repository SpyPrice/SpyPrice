# ETL (прототип сбора цен)

Однопроцессный ручной runner: загружает HTML карточек товара DNS / Ozon, пытается выделить цену и отправляет срез в backend через **internal** endpoint.

## Запуск

Рекомендуется через Docker Compose с profile `manual` (см. [`../README.md`](../README.md)).

Обязательно задать **`DEMO_ITEMS`**:

```text
<uuid_товара>|dns_html|https://www.dns-shop.ru/...;<uuid_товара>|ozon_html|https://www.ozon.ru/...
```

`parser_type` должен совпадать с полем источника (`dns_html` / `ozon_html`). UUID товара берётся из ответа `POST /api/v1/products` или из списка товаров.

## Переменные окружения

| Переменная | Описание |
|------------|----------|
| `API_BASE_URL` | Базовый URL API (в Docker: `http://backend:8000`) |
| `ETL_API_KEY` | Тот же ключ, что в backend (`X-ETL-API-Key`) |
| `DEMO_ITEMS` | Строка заданий (см. выше) |
| `REQUEST_TIMEOUT_SECONDS` | Таймаут HTTP (по умолчанию 20) |
| `MAX_RETRIES` | Число повторов при ошибке запроса |
| `FETCH_DELAY_SECONDS` | Пауза после каждой позиции |

## Ограничения

Парсинг **не гарантирует** корректную цену: используется общий regex по тексту страницы. Сайты могут блокировать роботов, показывать капчу или менять вёрстку.

Подробности: [`../docs/8. Реализация каркаса (Backend & ETL)/README.md`](../docs/8.%20Реализация%20каркаса%20(Backend%20&%20ETL)/README.md).
