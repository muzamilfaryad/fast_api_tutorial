# Deep Dive Examples

This folder contains more advanced FastAPI and Pydantic experiments, especially around runtime model generation.

## Main Idea

The examples build models dynamically with `pydantic.create_model()` based on the requested category or content type. That makes it easier to validate different payload shapes without hardcoding a separate schema for every case.

## What the Examples Show

- Dynamic product models created from category definitions.
- Dynamic content entry models created from model definitions.
- Runtime validation with Pydantic base models.
- The difference between static schemas and generated schemas.
- How to return structured validation errors from FastAPI routes.

## Files

- `main.py` - the full example application.

## Run

```bash
pip install fastapi uvicorn pydantic
uvicorn main:app --reload
```

## Why This Folder Exists

This is a learning sandbox for situations where one fixed request model is not enough. It is useful when category-specific or content-type-specific fields need to be validated at runtime.