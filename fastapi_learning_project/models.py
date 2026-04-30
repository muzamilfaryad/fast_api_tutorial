from pydantic import BaseModel, Field

# -------------------------
# ITEM MODEL (VALIDATION)
# -------------------------
class Item(BaseModel):
    name: str = Field(..., min_length=3, description="Item name must be at least 3 characters")
    price: float
    description: str | None = None

# -------------------------
# OFFER MODEL
# -------------------------
class Offer(BaseModel):
    discount: float = Field(..., gt=0, lt=100, description="Discount must be between 1 and 100")