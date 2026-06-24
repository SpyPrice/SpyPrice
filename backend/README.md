# Backend (FastAPI)

Сервис REST API для каркаса Price Tracker: пользователи, источники, товары, история цен, метрики, приём срезов от ETL.

Документация OpenAPI: `http://localhost:8000/docs`.

## Схема данных

app/schemas - Pydantic схемы
app/models - ORM для PostgreSQL

## Структура пакета `app`

api - взаимодействие с сервером, Backend <-> ETL
services - бизнес-логика
repository - взаимодействие с db

Поток данных: api -> services -> repository -> db
