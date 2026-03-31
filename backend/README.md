# Backend (FastAPI)

Сервис REST API для каркаса Price Tracker: пользователи, источники, товары, история цен, метрики, приём срезов от ETL.

## Запуск в разработке

Предпочтительно через корневой **Docker Compose** (см. [`../README.md`](../README.md)).

Локально (нужен PostgreSQL и переменные окружения):

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+asyncpg://USER:PASS@localhost:5432/price_tracker"
export JWT_SECRET="dev-secret"
export ETL_API_KEY="dev-etl"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Документация OpenAPI: `http://localhost:8000/docs`.

## Схема данных

![Схема данных](../docs/7.%20Technical%20Documentation/Actual-data-diagram.png)


## Структура пакета `app`

api - взаимодействие с сервером
services - бизнес-логика
repository - взаимодействие с db

Поток данных: api -> services -> repository -> db

## Важные переменные окружения

