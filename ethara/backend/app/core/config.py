from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://ethara:ethara@localhost:5432/ethara"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000", "http://localhost:80"]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
