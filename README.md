# Price Tracker — сервис отслеживания цен

Проект: **сервис для отслеживания и анализа изменения цен в онлайн‑магазинах** (MVP).

## Что делаем в MVP
- **Регистрация/вход** пользователя и личный кабинет.
- **Добавление товара по ссылке** (URL) и привязка к источнику (магазину).
- **Сбор цен** (планировщик/воркер), сохранение **истории**.
- **Просмотр истории** (график + таблица) и **базовые метрики** (min/max/avg/изменение за период).
- **(Опционально)** уведомления (порог/процент), простая аналитика (топ изменений).

## Репозиторий и ветвление
- **main**: стабильная ветка (демо/показы).
- Рабочий процесс: feature‑ветка → PR → ревью → merge в `main`.

## Документация (Obsidian)
Вся командная документация лежит в `docs/` и рассчитана на работу в Obsidian (или любом Markdown‑редакторе). **Оглавление и связь с официальным ТЗ** — в [`docs/README.md`](docs/README.md); полный текст задания — [`ТЗ.md`](ТЗ.md).

### Как работать в Obsidian
1. Установите Obsidian.
2. Откройте папку `price-tracker` как Vault (хранилище).
3. Установите плагин **Obsidian Git** (Community plugins).
4. Рекомендуемые настройки плагина:
   - **Auto commit**: каждые 10 минут
   - **Pull updates on startup**: включить
5. Папка `.obsidian/` добавлена в `.gitignore`, чтобы локальные настройки не конфликтовали между участниками.

## Как связать с GitHub (удалённый репозиторий)
1. Создайте репозиторий на GitHub (пустой).
2. В корне `price-tracker/` выполните:

```bash
git remote add origin <SSH_или_HTTPS_URL_вашего_репо>
git branch -M main
git push -u origin main
```

## GitHub Projects (основа)
Рекомендуется завести GitHub Project (Board/Kanban) и добавить поля:
- **Status**: Todo / In Progress / Done
- **Sprint**: Iteration (Weeks 1–3, 4–6, …)
- **Priority**: High / Medium / Low
- **Story Points**: Number

## Технический каркас (Лёша + Эдик)

Реализован backend + ETL каркас:
- `backend/` — FastAPI + PostgreSQL, JWT auth, CRUD товаров, история, метрики, internal ingest.
- `etl/` — прототип адаптеров `dns_html` и `ozon_html`, retry/timeout, вежливый User-Agent, отправка в backend.
- `docker-compose.yml` — запуск `db` + `backend`, ETL через профиль `manual`.

### Быстрый запуск

1. Скопируйте `.env.example` в `.env` и задайте секреты:
```bash
cp .env.example .env
```
2. Поднимите базу и API:
```bash
docker compose up --build -d db backend
```
3. Swagger:
`http://localhost:8000/docs`

### ETL (ручной прогон)

1. Создайте пользователя, добавьте товар через API и получите `product_id`.
2. В `.env` заполните `DEMO_ITEMS`:
```bash
DEMO_ITEMS=<product_id>|dns_html|https://www.dns-shop.ru/...;<product_id>|ozon_html|https://www.ozon.ru/...
```
3. Запустите ETL:
```bash
docker compose --profile manual run --rm etl
```

### Что защищено в ядре
- JWT для пользовательских endpoint'ов.
- Internal ingest защищен `X-ETL-API-Key`.
- История/метрики/CRUD доступны только владельцу товара.

