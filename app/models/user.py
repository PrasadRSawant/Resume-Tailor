# app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.schema import UniqueConstraint
from app.core.database import Base


class User(Base):
    """
    SQLAlchemy ORM model for the User entity.
    Defines the database schema, table name, and columns for a user.
    """
    __tablename__ = "users"  # Define the table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key, auto-incrementing
    username = Column(String, unique=True, index=True, nullable=False)  # Unique username
    email = Column(String, unique=True, index=True, nullable=False)  # Unique email address
    hashed_password = Column(String, nullable=False)  # Hashed password for security
    is_active = Column(Boolean, default=True, nullable=False)  # Account status (active/inactive)
    is_superuser = Column(Boolean, default=False, nullable=False)  # Superuser privileges

    # Optional: You can add relationships to other models here if needed.
    # For example:
    # items = relationship("Item", back_populates="owner")

    def __repr__(self):
        """
        Returns a string representation of the User object, useful for debugging.
        """
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

    # Ensure uniqueness across multiple columns if necessary, though for username/email
    # individual unique constraints are typically sufficient.
    # __table_args__ = (UniqueConstraint("username", "email", name="uq_username_email"),)
