from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated

from models import Item, Offer
from database import fake_db
from dependencies import get_db, get_current_user

app = FastAPI(title="FastAPI Learning Project")

# -------------------------
# GET API (Root)
# -------------------------
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Learning Project 🚀"}

# -------------------------
# PATH PARAMETER EXAMPLE
# -------------------------
@app.get("/items/{item_id}")
async def get_item(item_id: int, db: Annotated[dict, Depends(get_db)]):
    item = db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# -------------------------
# QUERY PARAMETER EXAMPLE
# -------------------------
@app.get("/search/")
async def search_item(name: str | None = None):
    if name:
        return {"result": f"Searching for {name}"}
    return {"result": "No search query provided"}

# -------------------------
# POST API (REQUEST BODY + VALIDATION)
# -------------------------
@app.post("/items/")
async def create_item(item: Item):
    new_id = max(fake_db.keys()) + 1
    fake_db[new_id] = item.model_dump()
    return {"id": new_id, "item": item}

# -------------------------
# POST WITH MULTIPLE BODY MODELS
# -------------------------
@app.post("/offer/")
async def create_offer(
    item: Item,
    offer: Offer,
    user: Annotated[str, Depends(get_current_user)]
):
    return {
        "user": user,
        "item": item,
        "offer": offer
    }