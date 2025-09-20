"""
API endpoints for User.
Uses FastAPI APIRouter to handle routes like /users, /users/{id},
delegating work to services.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# Import Pydantic schemas for request/response validation
from app.schemas.user import UserCreate, UserUpdate, User

# Import the business logic service for user operations
from app.services.user_service import UserService

# Import database dependency
# NOTE: get_db function is assumed to be defined in app/database.py
# This function will provide an AsyncSession to the services.
from app.database import get_db

# Initialize the FastAPI router for user-related endpoints
# The prefix "/users" means all routes defined in this router will start with /users
# The tag "Users" helps organize the documentation in FastAPI's interactive API docs (Swagger UI)
router = APIRouter(prefix="/users", tags=["Users"])

# Dependency to get an instance of UserService with an active database session
async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """
    Provides a UserService instance with an asynchronous database session.
    This function is a dependency that FastAPI will inject into our route handlers.
    """
    return UserService(db)

@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Registers a new user in the system with a unique username and email."
)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
) -> User:
    """
    Endpoint to create a new user.

    Args:
        user_data (UserCreate): The user data provided in the request body.
                                 Includes username, email, and password.
        user_service (UserService): Dependency-injected UserService for database operations.

    Raises:
        HTTPException: If a user with the given email or username already exists.

    Returns:
        User: The newly created user object, excluding the hashed password.
    """
    db_user = await user_service.get_user_by_username(username=user_data.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    db_user = await user_service.get_user_by_email(email=user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    created_user = await user_service.create_user(user_data)
    return created_user

@router.get(
    "/{user_id}",
    response_model=User,
    summary="Retrieve a user by ID",
    description="Fetches a single user's details using their unique user ID."
)
async def read_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
) -> User:
    """
    Endpoint to retrieve a user by their ID.

    Args:
        user_id (int): The unique identifier of the user to retrieve.
        user_service (UserService): Dependency-injected UserService.

    Raises:
        HTTPException: If no user with the given ID is found.

    Returns:
        User: The user object matching the provided ID.
    """
    db_user = await user_service.get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@router.get(
    "/",
    response_model=List[User],
    summary="Retrieve a list of users",
    description="Fetches a paginated list of all registered users."
)
async def read_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service)
) -> List[User]:
    """
    Endpoint to retrieve a list of users.

    Args:
        skip (int): The number of users to skip (for pagination). Defaults to 0.
        limit (int): The maximum number of users to return (for pagination). Defaults to 100.
        user_service (UserService): Dependency-injected UserService.

    Returns:
        List[User]: A list of user objects.
    """
    users = await user_service.get_users(skip=skip, limit=limit)
    return users

@router.put(
    "/{user_id}",
    response_model=User,
    summary="Update an existing user",
    description="Updates the details of an existing user identified by their ID."
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service)
) -> User:
    """
    Endpoint to update an existing user.

    Args:
        user_id (int): The unique identifier of the user to update.
        user_data (UserUpdate): The data to update the user with. Fields are optional.
        user_service (UserService): Dependency-injected UserService.

    Raises:
        HTTPException: If no user with the given ID is found.

    Returns:
        User: The updated user object.
    """
    db_user = await user_service.get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    updated_user = await user_service.update_user(db_user, user_data)
    return updated_user

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    description="Removes a user from the system permanently using their ID."
)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """
    Endpoint to delete a user.

    Args:
        user_id (int): The unique identifier of the user to delete.
        user_service (UserService): Dependency-injected UserService.

    Raises:
        HTTPException: If no user with the given ID is found.
    """
    db_user = await user_service.get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    await user_service.delete_user(db_user)
    # FastAPI automatically handles 204 No Content response for functions
    # that don't return anything specific.
    return None
