# FastAPI-E-Commarce Backend

FastAPI backend for the e-commerce tutorial project. It exposes versioned REST APIs for users, categories, products, reviews, background tasks, and order status updates.

## Highlights

- FastAPI application with custom validation error formatting.
- Separate routers for users, categories, products, reviews, and background task endpoints.
- CORS configured for the local Vite frontend.
- SQLModel and Alembic support for database work.
- Celery worker support for long-running order processing.

## Folder Structure

- `api/` - route modules for the public API.
- `core/` - settings, security, and database configuration.
- `crud/` - reusable database operations.
- `model/` - SQLModel table definitions.
- `alembic/` - migration environment and version history.
- `tasks.py` - background order processing task.
- `worker.py` - Celery application entry point.

## Requirements

- Python 3.10+ recommended.
- PostgreSQL running locally or reachable through the configured database URL.
- Redis if you want to run Celery tasks.

## Environment

Create a `.env` file in this folder with at least:

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/fastapi_ecom
DATABASE_SYNC_URL=postgresql+psycopg2://postgres:password@localhost:5432/fastapi_ecom
SECRET_KEY=change-me
ALGORITHM=HS256
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

## Install

```bash
pip install -r requirement.txt
```

## Run the API

```bash
alembic upgrade head
uvicorn main:app --reload
```

The API root endpoint is available at `/`, and the interactive docs are available at `/docs`.

## Run the Worker

If you are using the background order flow, start Celery in a separate terminal:

```bash
celery -A worker.celery_app worker --loglevel=info
```

## Notes

- The frontend origin is configured for `http://localhost:5173` and `http://127.0.0.1:5173`.
- The tutorial materials and playlist are intended as learning references, so some modules include verbose inline comments.
