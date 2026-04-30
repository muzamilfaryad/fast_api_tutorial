# ----------------------------
# IMPORTS
# ----------------------------

# FastAPI → main framework to build APIs
# Depends → used for Dependency Injection (DI)
# Header → used to read HTTP headers (like Authorization token)
from fastapi import FastAPI, Depends, Header

# Annotated → used to attach metadata (like dependency rules) to types
from typing import Annotated

# BaseModel → Pydantic class used for data validation & serialization
from pydantic import BaseModel   # official: used to define data schemas with type safety

# ----------------------------
# APP INSTANCE
# ----------------------------

# FastAPI() creates an application instance
# This object is used to define routes and handle requests
app = FastAPI()

# ============================================================
# 1. DATABASE DEPENDENCY (Dependency Injection Concept)
# ============================================================

"""
🔹 What is Dependency Injection (DI)?
Official FastAPI concept:
- A way to provide shared logic (like DB connection, auth, etc.)
- Automatically handled by FastAPI using Depends()

Easy Words:
👉 Instead of manually creating DB connection everywhere,
   FastAPI gives it automatically to your functions.
"""

async def get_db_session():
    # This function simulates a database connection/session

    print("Getting DB session")

    # Fake database structure (dictionary)
    session = {
        "data": {
            1: {"name": "Item 1"},
            2: {"name": "Item 2"}
        }
    }

    try:
        # yield means "give this value to route temporarily"
        # FastAPI will pause here and inject this session
        yield session

    finally:
        # finally runs after request is completed
        # used to close DB connection in real applications
        print("Closing DB session")


# Annotated[type, Depends(...)]
# → tells FastAPI: "inject this dependency automatically"
DBsession = Annotated[dict, Depends(get_db_session)]


# ============================================================
# 2. AUTH DEPENDENCY (Header + Token Concept)
# ============================================================

"""
🔹 What is Header?
Official:
- HTTP headers carry metadata like authentication tokens.

Easy:
👉 Browser sends extra info like token inside headers.
"""

async def get_user(token: Annotated[str | None, Header()] = None):

    # Header() tells FastAPI to read "token" from request headers
    # Example: token: abc123

    print("Checking auth ...")

    # In real apps:
    # - validate JWT token
    # - check database user
    # Here we just return a fake user

    return {"username": "test_user"}


# Dependency alias (clean reusable type)
CurrentUser = Annotated[dict, Depends(get_user)]


# ============================================================
# 3. PYDANTIC MODEL (DATA VALIDATION SCHEMA)
# ============================================================

"""
🔹 What is Pydantic BaseModel?
Official FastAPI definition:
- Used for data validation, parsing, and serialization

Easy Words:
👉 It ensures incoming data is correct type (str, float, etc.)
👉 Automatically converts JSON → Python object
"""

class Item(BaseModel):
    # name must be string
    name: str

    # price must be float (decimal number)
    price: float


# ============================================================
# 4. ROUTES (API ENDPOINTS)
# ============================================================

"""
🔹 What is a Route?
Official:
- A path + HTTP method that handles requests

Example:
POST /items/ → create item
GET /item/1 → read item
"""

# ----------------------------
# CREATE ITEM (POST REQUEST)
# ----------------------------
@app.post("/items/")
async def create_item(
    item: Item,   # Pydantic model (request body validation)
    db: DBsession,  # injected database dependency
    user: CurrentUser  # injected authenticated user
):

    print("Creating item for user:", user)

    # find last ID in DB and increment it
    new_id = max(db["data"].keys() or [0]) + 1

    # store item in fake database
    # item.dict() → converts Pydantic model → Python dict
    db["data"][new_id] = item.dict()

    # return response (FastAPI auto converts to JSON)
    return {"id": new_id, **item.dict()}


# ----------------------------
# READ ITEM (GET REQUEST)
# ----------------------------
@app.get("/item/{item_id}")
async def read_item(
    item_id: int,   # path parameter (URL variable)
    db: DBsession,  # DB injected
    user: CurrentUser  # user injected
):

    print("Reading item from DB for user:", user)

    # return item from database using ID
    return db["data"].get(item_id)