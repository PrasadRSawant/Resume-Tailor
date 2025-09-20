from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties for a user, used in creation and update
class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


# Properties to receive on user creation
class UserCreate(UserBase):
    username: str  # username is required for creation
    email: EmailStr  # email is required for creation
    password: str  # password is required for creation


# Properties to receive on user update
# All fields are optional for updates
class UserUpdate(UserBase):
    password: Optional[str] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: Optional[int] = None

    class ConfigDict:
        from_attributes = True  # Enable ORM mode to read data from SQLAlchemy models


# Properties to return to the API (e.g., when reading a user)
class User(UserInDBBase):
    pass


# Properties stored in DB, including password (used internally for authentication)
class UserInDB(UserInDBBase):
    hashed_password: str
