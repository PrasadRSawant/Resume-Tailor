
import pytest
from httpx import AsyncClient # For async tests with FastAPI, typically used with pytest-asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# --- MOCK/DUMMY IMPORTS AND SETUP FOR ISOLATED TESTING ---
# In a real project, you would import these from app.*.
# For the purpose of generating a self-contained test file,
# we create minimal mocks or assume their existence.

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timedelta
import jwt  # For mocking JWT creation and verification if not importing from app.utils.security
from passlib.context import CryptContext

# Minimalistic config settings for tests
class TestSettings:
    """Dummy settings for testing purposes."""
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"  # Use an in-memory or file-based SQLite for testing
    SECRET_KEY: str = "super-secret-test-key-replace-with-env"  # For JWT in tests
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

test_settings = TestSettings()

# Dummy security utils for testing purposes (mimics app.utils.security)
pwd_context_test = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash_test(password: str) -> str:
    """Hashes a password using bcrypt."""
    return pwd_context_test.hash(password)

def verify_password_test(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a hashed password."""
    return pwd_context_test.verify(plain_password, hashed_password)

def create_access_token_test(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=test_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, test_settings.SECRET_KEY, algorithm=test_settings.ALGORITHM)
    return encoded_jwt

def decode_access_token_test(token: str) -> Optional[dict]:
    """Decodes and verifies a JWT access token."""
    try:
        payload = jwt.decode(token, test_settings.SECRET_KEY, algorithms=[test_settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

# Dummy SQLAlchemy Base for models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
Base = declarative_base()

# Dummy User Model (mimics app.models.user.py)
class User(Base):
    """SQLAlchemy User model."""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"

# Dummy Pydantic Schemas (mimics app.schemas.user.py)
class UserBase(BaseModel):
    """Base Pydantic schema for user."""
    email: EmailStr

class UserCreate(UserBase):
    """Pydantic schema for creating a user."""
    password: str

class UserResponse(UserBase):
    """Pydantic schema for returning user data."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Dummy CRUD operations (mimics app.crud.user.py)
class CRUDUser:
    """CRUD operations for User model."""
    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        """Creates a new user in the database."""
        hashed_password = get_password_hash_test(user_in.password)
        db_user = User(email=user_in.email, hashed_password=hashed_password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Retrieves a user by email."""
        # Using text() for basic compatibility in dummy setup
        result = await db.execute(text("SELECT * FROM users WHERE email = :email").bindparams(email=email))
        return result.scalars().first()

    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> Optional[User]:
        """Retrieves a user by ID."""
        result = await db.execute(text("SELECT * FROM users WHERE id = :user_id").bindparams(user_id=user_id))
        return result.scalars().first()

    async def get_users(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        """Retrieves a list of users."""
        result = await db.execute(text("SELECT * FROM users LIMIT :limit OFFSET :skip").bindparams(limit=limit, skip=skip))
        return result.scalars().all()

    async def update_user(self, db: AsyncSession, db_user: User, user_update: UserCreate) -> User:
        """Updates an existing user."""
        # This is a simplified update, assumes UserCreate for update payload for simplicity in testing
        if user_update.email:
            db_user.email = user_update.email
        if user_update.password:
            db_user.hashed_password = get_password_hash_test(user_update.password)
        db_user.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def delete_user(self, db: AsyncSession, db_user: User):
        """Deletes a user from the database."""
        await db.delete(db_user)
        await db.commit()
        
crud_user = CRUDUser()

# Dummy Auth dependency (mimics app.dependencies.py and app.api.deps)
async def get_current_user_test(
    token: str = Depends(lambda: None), # In a real app, this would depend on OAuth2PasswordBearer
    db: AsyncSession = Depends(lambda: None) # In a real app, this would depend on get_db
) -> User:
    """Dummy dependency to get the current authenticated user from a token."""
    if token is None: # For cases where Depends(OAuth2PasswordBearer) would raise
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token_test(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_email = payload.get("sub")
    if user_email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await crud_user.get_user_by_email(db, email=user_email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Dummy User Router (mimics app.routers.users.py)
router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_new_user_route(user_in: UserCreate, db: AsyncSession = Depends(lambda: None)):
    """API endpoint to create a new user."""
    db_user = await crud_user.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud_user.create_user(db=db, user_in=user_in)

@router.get("/", response_model=List[UserResponse])
async def read_users_route(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(lambda: None),
    current_user: User = Depends(get_current_user_test) # Protect this route
):
    """API endpoint to retrieve a list of users."""
    users = await crud_user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def read_user_by_id_route(
    user_id: int,
    db: AsyncSession = Depends(lambda: None),
    current_user: User = Depends(get_current_user_test)
):
    """API endpoint to retrieve a specific user by ID."""
    db_user = await crud_user.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
async def update_existing_user_route(
    user_id: int,
    user_update: UserCreate, # Simplified, could be UserUpdate schema in real app
    db: AsyncSession = Depends(lambda: None),
    current_user: User = Depends(get_current_user_test)
):
    """API endpoint to update an existing user."""
    db_user = await crud_user.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    return await crud_user.update_user(db, db_user=db_user, user_update=user_update)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user_route(
    user_id: int,
    db: AsyncSession = Depends(lambda: None),
    current_user: User = Depends(get_current_user_test)
):
    """API endpoint to delete an existing user."""
    db_user = await crud_user.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    await crud_user.delete_user(db, db_user=db_user)
    return # No content for 204 HTTP status

# Main FastAPI app for testing, includes the dummy router
test_app = FastAPI()
test_app.include_router(router)

# --- TEST DATABASE SETUP ---
# Use an in-memory SQLite database for testing to ensure isolation and speed.
# In a real project, this might be configured in a conftest.py or similar.
TEST_DATABASE_URL = test_settings.DATABASE_URL
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def override_get_db():
    """Overrides the get_db dependency to use the test database."""
    async with TestingSessionLocal() as session:
        yield session

# Override dependencies that would normally inject a database session.
# We are using `Depends(lambda: None)` as a placeholder for `get_db` in our dummy routes.
test_app.dependency_overrides[Depends(lambda: None)] = override_get_db
# Ensure the get_current_user_test also uses the overridden database and its own logic.
# This might look redundant but ensures the dependency graph correctly uses the test functions.
test_app.dependency_overrides[get_current_user_test] = get_current_user_test

# --- PYTEST FIXTURES ---

@pytest.fixture(name="db_session")
async def db_session_fixture():
    """Provides a transactional scope for each test, creating and dropping tables."""
    # Create tables for the test database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Provide a session for the test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        await db.close()
        # Drop tables after the test
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(name="client")
def client_fixture(db_session: AsyncSession):
    """Provides a TestClient instance for making requests to the FastAPI app."""
    # The `db_session_fixture` already sets up the database, and `test_app.dependency_overrides`
    # points to `override_get_db` which uses `TestingSessionLocal`.
    # When `client` is created, it uses the `test_app` with its overrides.
    # The `db_session` parameter here ensures `db_session_fixture` runs before `client_fixture`.
    with TestClient(test_app) as client:
        yield client

# --- TEST CASES ---

@pytest.mark.asyncio
async def test_create_user(client: TestClient):
    """Test user creation with valid data."""
    user_data = {"email": "test@example.com", "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    created_user = UserResponse(**response.json())
    assert created_user.email == user_data["email"]
    assert created_user.id is not None
    assert created_user.is_active is True

@pytest.mark.asyncio
async def test_create_existing_user(client: TestClient):
    """Test creating a user with an already registered email."""
    user_data = {"email": "existing@example.com", "password": "password123"}
    client.post("/users/", json=user_data) # Create first user
    
    response = client.post("/users/", json=user_data) # Try to create again
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

@pytest.mark.asyncio
async def test_read_users_unauthenticated(client: TestClient):
    """Test reading users without authentication."""
    response = client.get("/users/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated" # As per our dummy get_current_user_test

@pytest.mark.asyncio
async def test_read_users_authenticated(client: TestClient, db_session: AsyncSession):
    """Test reading users with authentication."""
    user_data = {"email": "auth_user@example.com", "password": "password123"}
    create_response = client.post("/users/", json=user_data)
    assert create_response.status_code == 201
    created_user = UserResponse(**create_response.json())

    # Manually create an access token for the created user
    access_token = create_access_token_test(data={"sub": created_user.email})

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    users = [UserResponse(**u) for u in response.json()]
    assert len(users) >= 1 # At least the created user should be there
    assert any(u.email == created_user.email for u in users)

@pytest.mark.asyncio
async def test_read_user_by_id_authenticated(client: TestClient, db_session: AsyncSession):
    """Test reading a specific user by ID with authentication."""
    user_data = {"email": "user_by_id@example.com", "password": "password123"}
    create_response = client.post("/users/", json=user_data)
    assert create_response.status_code == 201
    created_user = UserResponse(**create_response.json())

    access_token = create_access_token_test(data={"sub": created_user.email})
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get(f"/users/{created_user.id}", headers=headers)
    assert response.status_code == 200
    read_user = UserResponse(**response.json())
    assert read_user.id == created_user.id
    assert read_user.email == created_user.email

@pytest.mark.asyncio
async def test_read_non_existent_user_by_id(client: TestClient, db_session: AsyncSession):
    """Test reading a non-existent user by ID."""
    user_data = {"email": "temp_user_for_non_exist@example.com", "password": "password123"}
    create_response = client.post("/users/", json=user_data)
    assert create_response.status_code == 201
    created_user = UserResponse(**create_response.json())

    access_token = create_access_token_test(data={"sub": created_user.email})
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/users/99999", headers=headers) # Non-existent ID
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_update_user_authenticated(client: TestClient, db_session: AsyncSession):
    """Test updating an authenticated user's own data."""
    user_data = {"email": "update_me@example.com", "password": "old_password"}
    create_response = client.post("/users/", json=user_data)
    assert create_response.status_code == 201
    created_user = UserResponse(**create_response.json())

    access_token = create_access_token_test(data={"sub": created_user.email})
    headers = {"Authorization": f"Bearer {access_token}"}

    updated_data = {"email": "updated_email@example.com", "password": "new_password"}
    response = client.put(f"/users/{created_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    updated_user = UserResponse(**response.json())
    assert updated_user.email == updated_data["email"]

    # Optional: Verify password change by fetching from DB and checking hash
    db_updated_user = await crud_user.get_user_by_id(db_session, user_id=updated_user.id)
    assert db_updated_user is not None
    assert verify_password_test(updated_data["password"], db_updated_user.hashed_password)


@pytest.mark.asyncio
async def test_update_other_user_authenticated(client: TestClient, db_session: AsyncSession):
    """Test updating another user's data (should be forbidden)."""
    user1_data = {"email": "user1@example.com", "password": "password1"}
    user2_data = {"email": "user2@example.com", "password": "password2"}

    create_response1 = client.post("/users/", json=user1_data)
    create_response2 = client.post("/users/", json=user2_data)
    assert create_response1.status_code == 201
    assert create_response2.status_code == 201

    user1 = UserResponse(**create_response1.json())
    user2 = UserResponse(**create_response2.json())

    # User 1 tries to update User 2
    access_token_user1 = create_access_token_test(data={"sub": user1.email})
    headers_user1 = {"Authorization": f"Bearer {access_token_user1}"}

    updated_data = {"email": "user2_new@example.com", "password": "new_password"}
    response = client.put(f"/users/{user2.id}", json=updated_data, headers=headers_user1)
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to update this user"

@pytest.mark.asyncio
async def test_delete_user_authenticated(client: TestClient, db_session: AsyncSession):
    """Test deleting an authenticated user's own account."""
    user_data = {"email": "delete_me@example.com", "password": "password"}
    create_response = client.post("/users/", json=user_data)
    assert create_response.status_code == 201
    created_user = UserResponse(**create_response.json())

    access_token = create_access_token_test(data={"sub": created_user.email})
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.delete(f"/users/{created_user.id}", headers=headers)
    assert response.status_code == 204

    # Verify user is truly deleted by trying to fetch
    fetch_response = client.get(f"/users/{created_user.id}", headers=headers)
    assert fetch_response.status_code == 404 # User not found

@pytest.mark.asyncio
async def test_delete_other_user_authenticated(client: TestClient, db_session: AsyncSession):
    """Test deleting another user's account (should be forbidden)."""
    user1_data = {"email": "deleter@example.com", "password": "password1"}
    user2_data = {"email": "to_be_deleted@example.com", "password": "password2"}

    create_response1 = client.post("/users/", json=user1_data)
    create_response2 = client.post("/users/", json=user2_data)
    assert create_response1.status_code == 201
    assert create_response2.status_code == 201

    user1 = UserResponse(**create_response1.json())
    user2 = UserResponse(**create_response2.json())

    # User 1 tries to delete User 2
    access_token_user1 = create_access_token_test(data={"sub": user1.email})
    headers_user1 = {"Authorization": f"Bearer {access_token_user1}"}

    response = client.delete(f"/users/{user2.id}", headers=headers_user1)
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to delete this user"

