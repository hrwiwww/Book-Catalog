# Book-Catalog

## Запуск локально

1. Перейти в директорию каталога:

```bash
cd library_catalog
```

2. Создать файл `.env`

```env
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/library_catalog
```

3. Поднять PostgreSQL через Docker Compose:

```bash
docker-compose up -d
```

4. Принять миграции Alembic:

```bash
poetry run alembic upgrade head
```

5. Запустить сервер:

```bash
poetry run uvicorn library_catalog.main:app --reload
```

После запуска API будет доступно по адресу: http://127.0.0.1:8000

- Документация Swagger UI: http://127.0.0.1:8000/docs
- Документация ReDoc: http://127.0.0.1:8000/redoc


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
