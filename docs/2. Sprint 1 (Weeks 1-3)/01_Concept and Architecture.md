# Концепция и архитектура (Sprint 1)

## Концепция
Мы строим сервис, который позволяет пользователю добавить ссылку на товар из онлайн‑магазина и получать:
- текущую цену и статус (в наличии/нет, если доступно),
- историю изменений цены,
- график динамики,
- базовые метрики (min/max/avg/изменение за период),
- (опционально) уведомления и лёгкую аналитику.

## Что важно для MVP
- 1–2 источника (магазина) с простым парсингом/доступным API.
- Вежливый сбор (rate limiting), учёт robots.txt и юридических ограничений.
- Минимально достаточный каркас: модели данных, API, прототип интерфейса, демонстрируемый сбор.

## Архитектурный набросок
- **Frontend (SPA)**: страницы логина/регистрации, дашборд товаров, карточка товара с графиком/историей.
- **Backend API**: авторизация, CRUD товаров, история цен, метрики; служебный приём PriceSnapshot.
- **ETL/Parser**: адаптеры под источники + планировщик запуска; нормализация; запись срезов.
- **DB**: PostgreSQL (User, Source, Product, PriceSnapshot, AlertRule/AlertEvent).

См. детали:
- [[API]] (в `7. Technical Documentation/API.md`)
- [[Database]] (в `7. Technical Documentation/Database.md`)
- [[Parser Architecture]] (в `7. Technical Documentation/Parser Architecture.md`)
- [[Contracts]] (в `7. Technical Documentation/Contracts.md`)
- [[01_Architecture Overview]] (в `7. Technical Documentation/01_Architecture Overview.md`)

