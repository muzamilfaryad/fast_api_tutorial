from typing import Annotated
from fastapi import Header, HTTPException

# -------------------------
# DATABASE DEPENDENCY
# -------------------------
def get_db():
    print("Connecting to DB...")
    return {
        1: {"name": "Laptop", "price": 1200},
        2: {"name": "Phone", "price": 800},
    }

# -------------------------
# AUTH DEPENDENCY (SIMPLIFIED)
# -------------------------
def get_current_user(x_token: Annotated[str | None, Header()] = None):
    if x_token != "secret-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return "muzamil"