# db.py

# ----------------------------
# IMPORTS
# ----------------------------

# Used to create an ASYNCHRONOUS database engine (connection to DB)
from sqlalchemy.ext.asyncio.engine import create_async_engine

# AsyncSession is used to interact with the database using async/await
from sqlmodel.ext.asyncio.session import AsyncSession

# sessionmaker is a factory used to create new session objects
from sqlalchemy.orm import sessionmaker

# Importing settings (where DATABASE_URL is stored, e.g., from .env file)
from .config import settings


# ----------------------------
# DATABASE ENGINE
# ----------------------------

# Engine = core connection to the database
# It manages connection pooling and communication with DB

engine = create_async_engine(
    settings.DATABASE_URL,  # Example: "postgresql+asyncpg://user:pass@localhost/db"
    echo=True               # Logs SQL queries in terminal (good for debugging)
)

# WHY async engine?
# → FastAPI is async → so DB operations should also be async
# → Improves performance when handling many users


# ----------------------------
# SESSION FACTORY
# ----------------------------

# sessionmaker creates a "factory" for making sessions
# Instead of manually creating sessions every time, we use this

AsyncSessionFactory = sessionmaker(
    engine,                 # Bind engine (connect sessions to DB)
    class_=AsyncSession,    # Use async session instead of normal session
    expire_on_commit=False  # Prevents data from being cleared after commit
)

# WHY expire_on_commit=False?
# → Normally, after saving data (commit), SQLAlchemy clears objects
# → This avoids needing to reload them again
# → Useful for APIs where you immediately return data


# ----------------------------
# DEPENDENCY FUNCTION (IMPORTANT FOR FASTAPI)
# ----------------------------

async def get_session():
    """
    This is a FastAPI dependency function.

    It:
    1. Creates a database session
    2. Provides it to the API endpoint
    3. Handles commit/rollback automatically
    4. Closes the session safely
    """

    # Create a session using the factory
    # "async with" ensures proper cleanup (like closing file automatically)
    async with AsyncSessionFactory() as session:

        try:
            # "yield" sends the session to the API endpoint
            # Example:
            # async def route(session: AsyncSession = Depends(get_session))
            yield session

            # If everything worked fine → save changes to DB
            await session.commit()

        except Exception:
            # If ANY error happens → undo all DB changes
            await session.rollback()

            # Re-raise error so FastAPI can show it
            raise

# ----------------------------
# KEY CONCEPT SUMMARY
# ----------------------------

# 1. ENGINE:
#    → Connects your app to database

# 2. SESSION:
#    → Used to run queries (SELECT, INSERT, UPDATE, DELETE)

# 3. SESSION FACTORY:
#    → Creates new sessions when needed

# 4. DEPENDENCY (get_session):
#    → Automatically gives session to routes
#    → Handles commit/rollback
#    → Prevents DB leaks (very important)

# ----------------------------
# HOW IT IS USED IN FASTAPI
# ----------------------------

# Example:

# from fastapi import Depends
#
# @app.get("/items")
# async def get_items(session: AsyncSession = Depends(get_session)):
#     result = await session.execute(...)
#     return result.fetchall()

# Flow:
# Request → get_session() → session created → used → commit/rollback → closed