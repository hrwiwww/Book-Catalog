# Book-Catalog

## Запуск локально

1. Перейдите в директорию приложения:

```bash
cd library_catalog
```

2. Создайте файл `.env` (см. пример ниже).

3. Поднимите PostgreSQL через Docker Compose:

```bash
docker-compose up -d
```

4. Примените миграции Alembic:

```bash
poetry run alembic upgrade head
```

5. Запустите сервер:

```bash
poetry run uvicorn library_catalog.main:app --reload
```

После запуска API будет доступно по адресу: http://127.0.0.1:8000

- Документация Swagger UI: http://127.0.0.1:8000/docs
- Документация ReDoc: http://127.0.0.1:8000/redoc

## Переменные окружения

Создайте файл `library_catalog/.env` с минимальным набором переменных:

```env
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/library_catalog
```

### Описание переменных

| Переменная | Обязательная | Описание |
|------------|--------------|----------|
| `ENVIRONMENT` | да | Окружение: `development`, `staging` или `production` |
| `DEBUG` | да | Режим отладки: `true` или `false` |
| `DATABASE_URL` | да | DSN для PostgreSQL с asyncpg, например `postgresql+asyncpg://user:password@host:port/dbname` |
| `DATABASE_POOL_SIZE` | нет | Размер пула подключений к БД (по умолчанию `20`) |
| `LOG_LEVEL` | нет | Уровень логирования: `DEBUG`, `INFO`, `WARNING`, `ERROR` (по умолчанию `INFO`) |
| `API_V1_PREFIX` | нет | Префикс API v1 (по умолчанию `/api/v1`) |
| `DOCS_URL` | нет | Путь к Swagger UI (по умолчанию `/docs`) |
| `REDOC_URL` | нет | Путь к ReDoc (по умолчанию `/redoc`) |
| `CORS_ORIGINS` | нет | Список разрешённых CORS-origins через запятую (по умолчанию `*`) |
| `OPENLIBRARY_BASE_URL` | нет | Базовый URL Open Library API (по умолчанию `https://openlibrary.org`) |
| `OPENLIBRARY_TIMEOUT` | нет | Таймаут запросов к Open Library в секундах (по умолчанию `10.0`) |

### Примечание по CORS

По умолчанию `CORS_ORIGINS=*`, а `allow_credentials` отключён. Если вы планируете использовать авторизацию через куки/заголовки, задайте конкретные origins, например:

```env
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## Запуск тестов

```bash
cd library_catalog
poetry run pytest
```

## Остановка

```bash
cd library_catalog
docker-compose down
```
