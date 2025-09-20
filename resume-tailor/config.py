from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    APP_NAME: str = "Resume Tailor API"
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()