# FastAPI Learning Project

This folder is a compact FastAPI practice project that demonstrates the basics of request handling and dependency injection.

## What You Will Find

- Path parameters with `GET /items/{item_id}`.
- Query parameters with `GET /search/`.
- Request body validation with Pydantic models.
- Multiple request body models in a single endpoint.
- Dependency injection for a fake database session and a simple auth token check.

## Files

- `main.py` - the FastAPI application and all example routes.
- `models.py` - Pydantic request schemas.
- `database.py` - in-memory sample data.
- `dependencies.py` - reusable dependency functions.
- `requirements.txt` - Python dependencies for the example.

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

Open `/docs` to explore the automatically generated Swagger UI.

## Learning Goals

- Understand how FastAPI reads data from the path, query string, headers, and request body.
- See how `Depends()` injects shared logic into route handlers.
- Practice Pydantic validation with real API inputs.