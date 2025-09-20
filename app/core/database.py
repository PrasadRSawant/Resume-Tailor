"""
Database connection handling using SQLAlchemy and async session.
Manages PostgreSQL engine and session lifecycle.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import settings

# Determine the asynchronous database URL based on the configured DATABASE_URL.
# If using SQLite, we adjust the URL to use `aiosqlite` driver.
# For PostgreSQL, it will typically be `postgresql+asyncpg://...`.
if settings.DATABASE_URL.startswith("sqlite+aiosqlite"):
    ASYNC_DATABASE_URL = settings.DATABASE_URL
elif settings.DATABASE_URL.startswith("sqlite:///"):
    # If the user provided a synchronous SQLite URL, convert it to async.
    ASYNC_DATABASE_URL = settings.DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
elif settings.DATABASE_URL.startswith("postgresql://"):
    ASYNC_DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
else:
    ASYNC_DATABASE_URL = settings.DATABASE_URL

# Create an asynchronous engine for database interaction.
# `pool_pre_ping=True` ensures that connections are alive before being used from the pool.
# `echo=True` will log all SQL statements, useful for debugging (set to False in production).
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=settings.DEBUG_MODE,  # Log SQL statements if debug mode is on
    pool_pre_ping=True
)

# Create an asynchronous session factory.
# `expire_on_commit=False` prevents objects from being expired after commit,
# which can be useful when objects are still needed after a transaction.
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for declarative models. All SQLAlchemy models will inherit from this.
Base = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to provide an asynchronous database session.

    This function creates a new async session, yields it to the calling function,
    and ensures it is closed after the request is finished.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
