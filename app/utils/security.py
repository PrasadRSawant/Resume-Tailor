# app/utils/security.py

from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from jose import JWTError, jwt

# Password hashing configuration
# Using bcrypt for password hashing, which is a strong and widely recommended hashing algorithm.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Password Hashing Functions ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a hashed password.

    Args:
        plain_password (str): The password provided by the user (not hashed).
        hashed_password (str): The password hash stored in the database.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        str: The hashed password string.
    """
    return pwd_context.hash(password)

# --- JWT Token Configuration and Functions ---

# IMPORTANT: In a production environment, these values MUST be loaded from
# environment variables (e.g., using `python-dotenv` or a configuration management system)
# and NEVER hardcoded. The SECRET_KEY should be a long, random string.
SECRET_KEY = "your-super-secret-key-that-should-be-at-least-32-characters-long-and-random"
ALGORITHM = "HS256" # HS256 is a common and secure algorithm for symmetric keys
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Access token will expire after 30 minutes

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token.

    Args:
        data (dict): The payload to encode into the token (e.g., {"sub": user_email}).
        expires_delta (Optional[timedelta]): Optional timedelta for token expiration.
                                            If None, uses ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: The encoded JWT token string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # Add expiration time to the payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodes a JWT access token and returns its payload if valid.

    Args:
        token (str): The JWT token string to decode.

    Returns:
        Optional[dict]: The decoded payload dictionary if the token is valid and not expired.
                        Returns None if the token is invalid (e.g., bad signature, expired).
    Raises:
        JWTError: If the token cannot be decoded or verified (e.g., invalid signature, malformed token).
                  In a real application, you might catch this and raise an HTTPException.
    """
    try:
        # Decode the token, verifying its signature and expiration
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        # Log the specific JWT error (e.g., ExpiredSignatureError, InvalidSignatureError)
        # For security, avoid returning detailed error messages to the client.
        print(f"JWT Decoding Error: {e}")
        return None

# Note: The actual FastAPI dependency for getting the current authenticated user
# from a request header (e.g., `get_current_user`) typically uses `OAuth2PasswordBearer`
# and interacts with `UserService`. This dependency is usually defined in `app/dependencies.py`.
