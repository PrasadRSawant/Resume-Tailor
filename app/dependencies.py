"""
app/dependencies.py

Houses reusable dependencies like database session, authentication, or common utilities injected into routes.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
# Assuming you have a database configuration in app.database.
# This import will need to be adjusted based on your actual database module structure.
# For example, if your database setup is in 'app/core/database.py', then
# from app.core.database import AsyncSessionLocal
from app.database import AsyncSessionLocal # Placeholder: Adjust import path as needed

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an asynchronous database session.

    This generator function creates a new SQLAlchemy AsyncSession,
    yields it to the route function, and ensures it is closed
    after the request is finished, even if errors occur.
    """
    db: AsyncSession = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

# You can add other dependencies here, for example, for authentication:
# async def get_current_user():
#     # Implement user authentication logic here
#     pass

# async def get_current_active_user():
#     # Implement active user authentication logic here
#     pass
