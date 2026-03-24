# Backend (FastAPI)

Сервис REST API для каркаса Price Tracker: пользователи, источники, товары, история цен, метрики, приём срезов от ETL.

## Запуск в разработке

Предпочтительно через корневой **Docker Compose** (см. [`../README.md`](../README.md)).

Локально (нужен PostgreSQL и переменные окружения):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://USER:PASS@localhost:5432/price_tracker"
export JWT_SECRET="dev-secret"
export ETL_API_KEY="dev-etl"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Документация OpenAPI: `http://localhost:8000/docs`.

## Структура пакета `app`

| Файл | Назначение |
|------|------------|
| `main.py` | FastAPI-приложение, маршруты, сид источников при старте |
| `models.py` | SQLAlchemy: `User`, `Source`, `Product`, `PriceSnapshot` |
| `schemas.py` | Pydantic-модели запросов/ответов |
| `database.py` | Engine, `SessionLocal`, `get_db` |
| `config.py` | Настройки из env (см. `Settings`) |
| `security.py` | Bcrypt, JWT create/decode |
| `deps.py` | `get_current_user`, `validate_etl_key` |

## Важные переменные окружения

См. класс `Settings` в `app/config.py`. Имена в верхнем регистре для Docker обычно: `DATABASE_URL`, `JWT_SECRET`, `ETL_API_KEY`, `CORS_ORIGINS`. Опционально файл `.env` в каталоге запуска процесса.

## Полная документация по каркасу

[`../docs/8. Реализация каркаса (Backend & ETL)/README.md`](../docs/8.%20Реализация%20каркаса%20(Backend%20&%20ETL)/README.md)
