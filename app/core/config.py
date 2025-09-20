from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    Centralized configuration management for the FastAPI application.
    Loads environment variables using Pydantic Settings for easy and secure access.
    """

    # Application settings
    APP_NAME: str = "FastAPI Project"
    APP_VERSION: str = "0.0.1"
    DEBUG_MODE: bool = False

    # Database settings
    DATABASE_URL: str = "sqlite:///./sql_app.db" # Default to SQLite for local development
    # Example for PostgreSQL: "postgresql://user:password@host:port/database"
    # Example for MySQL: "mysql+pymysql://user:password@host:port/database"

    # Security settings
    SECRET_KEY: str = "super-secret-key"  # IMPORTANT: Change this in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS settings (if needed)
    CORS_ORIGINS: list[str] = ["*"] # Adjust for production (e.g., ["http://localhost:3000"])
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # Pydantic Settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",            # Load environment variables from a .env file
        env_file_encoding="utf-8",  # Specify encoding for the .env file
        extra="ignore"              # Ignore extra environment variables not defined here
    )

# Create a settings instance for easy import throughout the application
settings = Settings()

# Example usage (for demonstration, normally not in config file itself)
# if __name__ == "__main__":
#     print("Application Name:", settings.APP_NAME)
#     print("Debug Mode:", settings.DEBUG_MODE)
#     print("Database URL:", settings.DATABASE_URL)
#     print("Secret Key:", settings.SECRET_KEY)
