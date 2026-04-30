# ============================================================
# ENTRY POINT (Python standard concept)
# ============================================================

# This block runs ONLY when you execute this file directly
# (NOT when imported as a module)
# It is a standard Python concept (not FastAPI-specific)

# if __name__ == "__main__":
#     print("Hello, World!")



# ============================================================
# FASTAPI BASIC SETUP
# ============================================================

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# FastAPI instance
# 👉 This creates your web application
# According to FastAPI docs:
# FastAPI() is the main class used to create APIs
app = FastAPI()



# ============================================================
# PYDANTIC MODEL (DATA VALIDATION)
# ============================================================

# BaseModel (from Pydantic)
# 👉 Used to define structure of data
# 👉 Automatically validates input data

class Item(BaseModel):
    # name must be string
    name: str

    # price must be float
    price: float

    # Optional means it can be None (not required)
    tax: Optional[float] = None


# 🔹 EASY EXPLANATION:
# This class ensures:
# ✔ name is always text
# ✔ price is always number
# ✔ tax is optional


# ============================================================
# SIMPLE GET APIs
# ============================================================

# GET API → used to FETCH data

@app.get("/message")
async def read_root():
    # async → allows high performance (non-blocking)
    # returns JSON response
    return {"Hello": "World"}


@app.get("/name")
async def read_name():
    return {"Hello": "Name"}



# ============================================================
# PATH PARAMETERS (COMMENTED EXAMPLES)
# ============================================================

# Path parameter → value comes from URL

# Example:
# http://127.0.0.1:8000/items/laptop

# @app.get("/items/{item_name}")
# async def get_items(item_name: str, q: Optional[float] = None):
#     return {"Hello": item_name, "q": q}


# Query parameter example:
# http://127.0.0.1:8000/items/laptop?company=HP

# @app.get("/items/{item_name}")
# async def get_items(item_name: str, company: Optional[str] = None):
#     return {"Hello": item_name, "company": company}


# ============================================================
# PAGINATION (skip + limit)
# ============================================================

# Used to control large data
# skip → how many items to skip
# limit → how many to return

# @app.get("/items/")
# async def all_items(skip: int = 0, limit: int = 10):
#     dummmy_data = [{"item_name": "item1"}, {"item_name": "item2"}, {"item_name": "item3"}, {"item_name": "item4"}, {"item_name": "item5"},
#                     {"item_name": "item6"}, {"item_name": "item7"}, {"item_name": "item8"}, {"item_name": "item9"}, {"item_name": "item10"}, {"item_name": "item11"}]
#
#     # slicing (Python concept)
#     # [start : end]
#     return dummmy_data[skip: skip + limit]


# ============================================================
# CURRENT ACTIVE ENDPOINT (IMPORTANT)
# ============================================================

@app.get("/items/")
async def all_items(skip: int = 0, limit: int = 10):

    # dictionary (raw data)
    data_dict = {
        "name": "Sample Item",
        "price": 100,
        "offer": 100   # ⚠️ NOTE: This field is NOT in Item model
    }

    # ❗ IMPORTANT CONCEPT:
    # Items(**data_dict)
    # 👉 This converts dictionary into Pydantic object

    # ❗ BUT:
    # "offer" is NOT defined in Item model
    # So Pydantic will ignore it (by default)

    return Item(**data_dict)



# ============================================================
# WHAT IS PYDANTIC?
# ============================================================

# Official idea:
# 👉 Data validation + parsing using Python type hints

# EASY WORDS:
# 👉 It checks if your data is correct or not

# Example:
# If price = "abc"
# ❌ Error
# If price = 100
# ✅ Valid


# ============================================================
# VALIDATION WITHOUT BaseModel
# ============================================================

# Using validate_call (function validation)

# from pydantic import validate_call, ValidationError
# from typing import Annotated

# @validate_call
# def validate_name(name: Annotated[str, Field(min_length=4)]):
#     return name

# try:
#     name = validate_name(name="Ali")  # ❌ too short
# except ValidationError as error:
#     print(error)



# ============================================================
# VALIDATION USING BaseModel
# ============================================================

# from pydantic import Field

# class Items(BaseModel):
#     name: str = Field(..., min_length=4)  # required + validation
#     description: str | None = None
#     price: float

# Field(...)
# 👉 used to add validation rules


# ============================================================
# INCLUDE / EXCLUDE (IMPORTANT INTERVIEW TOPIC)
# ============================================================

# product.model_dump(exclude={"price"})
# 👉 removes price from output

# product.model_dump(include={"name"})
# 👉 returns only name

# Useful for:
# ✔ hiding sensitive data
# ✔ customizing API response


# ============================================================
# PAYLOAD (VERY IMPORTANT)
# ============================================================

# Payload = actual data sent in request

# Example JSON:
# {
#   "name": "Laptop",
#   "price": 1000
# }

# 👉 This is payload


# ============================================================
# BODY VS PYDANTIC
# ============================================================

# Using Body (manual way)
# You define each field separately

# Using BaseModel (recommended)
# You define structure once → reuse everywhere



# ============================================================
# FINAL PART (POST API)
# ============================================================

from fastapi import Body
from typing import Annotated
from pydantic import Field


class Items(BaseModel):
    name: str = Field(..., min_length=4)
    description: str | None = None
    price: float


class Offer(BaseModel):
    name: str = Field(..., min_length=4)
    description: str | None = None
    price: float
    offer: float | None = None


@app.post("/items/")
async def create_item(

    # item → JSON body mapped to Items model
    item: Items = Body(...),

    # offer → second object in request body
    offer: Offer = Body(...),

    # Annotated → modern way to define metadata
    # same as: flower: str = Body(...)
    flower: Annotated[str, Body(...)] = ...
):

    # returning structured response
    return {
        "item": item,
        "offer": offer,
        "flower": flower
    }



# ============================================================
# SUMMARY (VERY IMPORTANT)
# ============================================================

# FastAPI:
# 👉 Framework to build APIs quickly

# Pydantic:
# 👉 Validates and structures data

# BaseModel:
# 👉 Defines data shape

# Field:
# 👉 Adds rules (min_length, etc.)

# Body:
# 👉 Reads data from request

# Payload:
# 👉 Actual data sent by client

# async:
# 👉 Makes API fast and scalable
