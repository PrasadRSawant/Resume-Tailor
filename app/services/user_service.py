from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    """
    Service layer for managing user-related business logic.
    Handles operations like creating, retrieving, updating, and deleting users.
    Interacts with database models and applies business rules.
    """

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hashes a plain-text password."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifies a plain-text password against a hashed password."""
        return pwd_context.verify(plain_password, hashed_password)

    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        """
        Creates a new user in the database.

        Args:
            db (AsyncSession): The asynchronous database session.
            user_in (UserCreate): Pydantic schema for user creation data.

        Returns:
            User: The newly created User ORM model.
        """
        hashed_password = self.get_password_hash(user_in.password)
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_password,
            is_active=user_in.is_active,
            is_superuser=user_in.is_superuser,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def get_user_by_id(self, db: AsyncSession, user_id: UUID) -> Optional[User]:
        """
        Retrieves a user by their ID.

        Args:
            db (AsyncSession): The asynchronous database session.
            user_id (UUID): The unique identifier of the user.

        Returns:
            Optional[User]: The User ORM model if found, otherwise None.
        """
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """
        Retrieves a user by their email address.

        Args:
            db (AsyncSession): The asynchronous database session.
            email (str): The email address of the user.

        Returns:
            Optional[User]: The User ORM model if found, otherwise None.
        """
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()
    
    async def get_user_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        """
        Retrieves a user by their username.

        Args:
            db (AsyncSession): The asynchronous database session.
            username (str): The username of the user.

        Returns:
            Optional[User]: The User ORM model if found, otherwise None.
        """
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalars().first()


    async def get_users(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Retrieves a list of users with pagination.

        Args:
            db (AsyncSession): The asynchronous database session.
            skip (int): Number of records to skip.
            limit (int): Maximum number of records to return.

        Returns:
            List[User]: A list of User ORM models.
        """
        result = await db.execute(select(User).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update_user(
        self, db: AsyncSession, user_id: UUID, user_update: UserUpdate
    ) -> Optional[User]:
        """
        Updates an existing user's information.

        Args:
            db (AsyncSession): The asynchronous database session.
            user_id (UUID): The ID of the user to update.
            user_update (UserUpdate): Pydantic schema for user update data.

        Returns:
            Optional[User]: The updated User ORM model if found, otherwise None.
        """
        db_user = await self.get_user_by_id(db, user_id)
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        
        # Handle password update separately
        if "password" in update_data and update_data["password"]:
            db_user.hashed_password = self.get_password_hash(update_data["password"])
            del update_data["password"] # Remove from dict to avoid direct assignment

        for key, value in update_data.items():
            setattr(db_user, key, value)

        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def delete_user(self, db: AsyncSession, user_id: UUID) -> bool:
        """
        Deletes a user from the database.

        Args:
            db (AsyncSession): The asynchronous database session.
            user_id (UUID): The ID of the user to delete.

        Returns:
            bool: True if the user was deleted, False if not found.
        """
        db_user = await self.get_user_by_id(db, user_id)
        if not db_user:
            return False
        await db.delete(db_user)
        await db.commit()
        return True

