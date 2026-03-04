from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./address_book.db"

    # API
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Address Book API"

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # or "text"
    log_file: Optional[str] = None # Log file path

    # Geocoding
    geocoding_timeout: int = 5  # seconds
    default_distance_unit: str = "km"

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()