"""
Application configuration file.
Loads environment variables and centralizes app settings.
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://username:password@localhost:5432/inventory_db"

    class Config:
        env_file = ".env"

settings = Settings()
