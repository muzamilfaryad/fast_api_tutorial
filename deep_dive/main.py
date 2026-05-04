#Problem was that we had a single ProductModel which could not represent all categories (Laptop, T-Shirt, Equipment) 
# because they have different fields. This led to validation errors and inflexible code.
#Solution: We created a function get_product_model_for_category that dynamically builds a Pydantic model based on the category_id. 
# This allows us to validate different product structures at runtime without hardcoding models for each category.


# Import FastAPI core tools
from fastapi import FastAPI, Depends, HTTPException, status

# create_model → used to dynamically create models at runtime
# BaseModel → base class for all Pydantic models
# Field → used for validation rules (e.g., gt=0)
from pydantic import create_model, BaseModel, Field

# Typing utilities
from typing import Any, Dict, Type, List, Literal

# Used for date validation
from datetime import date

# Create FastAPI app instance
app = FastAPI()


# -------------------------------------------
# 📦 CATEGORY DEFINITIONS (Simulating Database)
# -------------------------------------------
# In real applications, this comes from DB tables
# Each category has:
# 1. name
# 2. fields (with type + validation rules)

CATEGORY_DEFINITIONS = {
    1: {
        "name": "Laptop",
        "fields": {
            "cpu_type": (str, ...),   # required field (...)
            "ram_gb": (int, ...)      # required field
        }
    },
    2: {
        "name": "T-Shirt",
        "fields": {
            "color": (str, ...),
            # Literal restricts allowed values
            "size": (Literal['S','M','L','XL'], ...)
        }
    },
    3: {
        "name": "Equipment",
        "fields": {
            "voltage": (int, 220),  # default value = 220
            "warranty_expires_on": (date, ...)
        }
    }
}


# -------------------------------------------------------
# 🧠 FUNCTION: CREATE DYNAMIC PYDANTIC MODEL
# -------------------------------------------------------
def get_product_model_for_category(category_id: int) -> Type[BaseModel]:
    """
    This function dynamically creates a Pydantic model
    based on category_id.

    WHY?
    Because each category has different fields.
    """

    # Get category from "database"
    category = CATEGORY_DEFINITIONS.get(category_id)

    # If category does not exist → raise error
    if not category:
        raise HTTPException(
            status_code=404,
            detail=f"Product category {category_id} not found."
        )

    # -------------------------------------------
    # COMMON FIELDS (FOR ALL PRODUCTS)
    # -------------------------------------------
    base_fields = {
        'sku': (str, ...),  # required
        'price': (float, Field(..., gt=0))  # must be > 0
    }

    # -------------------------------------------
    # MERGE COMMON + CATEGORY-SPECIFIC FIELDS
    # -------------------------------------------
    all_fields = {
        **base_fields,
        **category["fields"]
    }

    # -------------------------------------------
    # 🔥 CREATE MODEL DYNAMICALLY
    # -------------------------------------------
    ProductModel = create_model(
        f'Dynamic{category["name"]}Model',  # dynamic class name
        **all_fields                        # unpack fields
    )

    # Return dynamically created class
    return ProductModel


# -------------------------------------------------------
# 📥 POST API → CREATE PRODUCT
# -------------------------------------------------------
@app.post("/products/{category_id}")
async def create_dynamic_product(
        category_id: int,
        request_body: Dict[str, Any]   # raw JSON input
):
    """
    This endpoint:
    1. Gets category
    2. Builds dynamic model
    3. Validates request
    """

    # Get dynamic model for category
    Model = get_product_model_for_category(category_id)

    try:
        # Validate request body using dynamic model
        validate_product = Model(**request_body)

    except Exception as error:
        # If validation fails → return 422
        raise HTTPException(status_code=422, detail=error)

    # If valid → return success
    return {
        "message": "Product created successfully",
        "product": validate_product.model_dump()  # convert model → dict
    }


# -------------------------------------------------------
# 🗄️ FAKE DATABASE
# -------------------------------------------------------
PRODUCT_DATABASE = {
    101: {
        "category_id": 1,
        "sku": "DELL-XPS-15",
        "price": 1899.99,
        "attributes": {
            "cpu_type": "Intel i9",
            "ram_gb": 32
        }
    },
    202: {
        "category_id": 2,
        "sku": "PLAIN-WHITE-T",
        "price": 15.50,
        "attributes": {
            "color": "White",
            "size": "L"
        }
    },
    303: {
        "category_id": 3,
        "sku": "CNC-MILL-01",
        "price": 75000.00,
        "attributes": {
            "voltage": 220,
            "warranty_expires_on": "2027-12-31"
        }
    }
}


# -------------------------------------------------------
# 📤 GET SINGLE PRODUCT
# -------------------------------------------------------
@app.get("/products/{product_id}")
async def get_product(product_id):
    """
    This endpoint:
    1. Fetches product
    2. Builds dynamic response model
    3. Validates response before returning
    """

    # Fetch product from database
    product_data = PRODUCT_DATABASE[int(product_id)]

    if not product_data:
        raise HTTPException(status_code=404, detail="Product does not exist")

    # Get category
    category_id = product_data["category_id"]

    # Build dynamic response model
    ResponseModel = get_product_model_for_category(category_id)

    # Merge base + attributes
    response_data = {
        "sku": product_data["sku"],
        "price": product_data["price"],
        **product_data["attributes"]
    }

    try:
        # Validate response before returning
        return ResponseModel(**response_data)

    except Exception as error:
        raise HTTPException(status_code=422, detail=f"{error}")


# -------------------------------------------------------
# 📋 GET ALL PRODUCTS
# -------------------------------------------------------
@app.get("/products", response_model=List[Dict[str, Any]])
async def get_all_products():
    """
    Returns all products (RAW DATA).

    ⚠️ Note:
    No dynamic validation here because:
    - Each product has different structure
    - One single response_model cannot represent all
    """

    return list(PRODUCT_DATABASE.values())




#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------

# -------------------------------------------------------
# 📦 CONTENT MODELS (Simulating Database)
# -------------------------------------------------------
# In real applications, this comes from DB tables
# Each content model has:
# 1. name
# 2. fields (with type + validation rules)

CONTENT_MODELS = {
    "blog_post": {
        "name": "Blog Post",
        "fields": {
            "title": (str, Field(..., min_length=3, max_length=100)),
            "author_id": (int, ...),
            "tags": (List[str], None)
        }
    },
    "author_profile": {
        "name": "Author Profile",
        "fields": {
            "full_name": (str, ...),
            "biography": (str, Field(..., max_length=500))
        }
    }
}


# -------------------------------------------------------
# 🧠 FUNCTION: CREATE DYNAMIC CONTENT MODEL
# -------------------------------------------------------
def get_content_entry_model(model_id: str) -> Type[BaseModel]:
    """
    This function dynamically creates a Pydantic model
    based on model_id.

    WHY?
    Because each content model has different fields.
    """

    # Get model from "database"
    model_info = CONTENT_MODELS.get(model_id)

    # If model does not exist → raise error
    if not model_info:
        raise HTTPException(
            status_code=404,
            detail=f"Content model {model_id} not found."
        )

    # -------------------------------------------
    # COMMON FIELDS (FOR ALL CONTENT)
    # -------------------------------------------
    base_fields = {
        "entry_id": (str, Field(default_factory=lambda: str(uuid.uuid4())))
    }

    # -------------------------------------------
    # MERGE COMMON + MODEL-SPECIFIC FIELDS
    # -------------------------------------------
    all_fields = {
        **base_fields,
        **model_info["fields"]
    }

    # -------------------------------------------
    # 🔥 CREATE MODEL DYNAMICALLY
    # -------------------------------------------
    ContentModel = create_model(
        model_info["name"],  # dynamic class name
        **all_fields                        # unpack fields
    )

    # Return dynamically created class
    return ContentModel


# -------------------------------------------------------
# 📥 POST API → CREATE CONTENT ENTRY
# -------------------------------------------------------
@app.post("/entries/{model_id}")
async def create_content_entry(model_id: str, data: BaseModel = Depends(get_content_entry_model)):
    """
    This endpoint:
    1. Gets model
    2. Builds dynamic model
    3. Validates request
    """

    # Get dynamic model for model_id
    Model = get_content_entry_model(model_id)

    try:
        # Validate request body using dynamic model
        validate_entry = Model(**data)

    except Exception as error:
        # If validation fails → return 422
        raise HTTPException(status_code=422, detail=error)

    # If valid → return success
    return {
        "message": "Content entry created successfully!",
        "model_id": model_id,
        "data": validate_entry.model_dump()  # convert model → dict
    }


