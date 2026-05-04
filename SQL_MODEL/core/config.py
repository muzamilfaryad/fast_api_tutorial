# Import BaseSettings from pydantic_settings
# This is used to manage application configuration (like environment variables)
from pydantic_settings import BaseSettings


# Create a Settings class that inherits from BaseSettings
# This class will automatically read values from environment variables (.env file)
class Settings(BaseSettings):

    # ----------------------------
    # DATABASE CONFIGURATION
    # ----------------------------

    # Async database URL (used with async frameworks like FastAPI + async SQLAlchemy)
    # Format:
    # postgresql+asyncpg://username:password@host:port/database_name
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgress@localhost:5432/fastapi_ecom"

    # Sync database URL (used with normal blocking code or tools like Alembic migrations)
    # psycopg2 is a synchronous PostgreSQL driver
    DATABASE_SYNC_URL: str = "postgresql+psycopg2://postgres:postgress@host.docker.internal:5432/fastapi_ecom"


    # ----------------------------
    # SECURITY CONFIGURATION
    # ----------------------------

    # SECRET_KEY is used for security purposes (e.g., JWT token signing)
    # No default value is provided → it MUST come from .env file
    SECRET_KEY: str

    # ALGORITHM used for encoding/decoding JWT tokens (e.g., HS256)
    # Also required from .env file
    ALGORITHM: str


    # ----------------------------
    # INNER CONFIG CLASS
    # ----------------------------

    class Config:
        # This tells Pydantic to load environment variables from a file named ".env"
        # Example: SECRET_KEY=your_secret_here
        env_file = ".env"


# ----------------------------
# CREATE INSTANCE
# ----------------------------

# This creates an object of Settings class
# It automatically:
# 1. Reads values from .env file
# 2. Overrides default values if env variables exist
# 3. Validates types (e.g., ensures strings are strings)
settings = Settings()