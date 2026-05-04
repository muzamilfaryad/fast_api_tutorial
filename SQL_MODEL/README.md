# SQL_MODEL

This folder contains a larger FastAPI backend built with SQLModel, Alembic migrations, JWT-style auth helpers, and Celery-based background processing.

## What It Includes

- SQLModel table definitions for users, categories, products, reviews, and orders.
- Separate API routers for core features.
- CRUD helpers for reusable database operations.
- Core configuration, database, auth, and security utilities.
- Alembic migrations for schema changes.
- Background order processing through a Celery worker.

## Folder Structure

- `api/` - route modules for users, products, categories, reviews, and background tasks.
- `CRUD/` - database helper functions.
- `core/` - settings, auth, security, and database wiring.
- `model/` - SQLModel table definitions.
- `alembic/` - migration configuration and version files.
- `main.py` - application entry point.
- `tasks.py` - background processing logic.
- `worker.py` - Celery configuration.

## Requirements

- Python 3.10+ recommended.
- PostgreSQL for persistence.
- Redis if you plan to run the worker.

## Install

```bash
pip install -r requirement.txt
```

## Environment

Create a `.env` file with the values expected by `core/config.py`. At minimum, define:

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/fastapi_sqlmodel
SECRET_KEY=change-me
ALGORITHM=HS256
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

## Run the API

```bash
alembic upgrade head
uvicorn main:app --reload
```

## Run the Worker

```bash
celery -A worker.celery_app worker --loglevel=info
```

## Notes

- The models and schemas are split so database tables and API payloads can evolve independently.
- The order-processing task is intentionally simple and demonstrates how a long-running job can update database state over time.