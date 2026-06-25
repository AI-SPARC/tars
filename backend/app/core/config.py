from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the TARS backend."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    project_name: str = "TARS"
    service_name: str = "tars-backend"
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    database_url: str = "sqlite+aiosqlite:///./tars.db"
    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    mqtt_enabled: bool = False
    mqtt_interface_name: str = "vda5050"
    vda5050_major_version: str = "v3"
    vda5050_protocol_version: str = "3.0.0"
    backend_cors_origins: str = Field(default="http://localhost:5173,http://localhost:8080")


@lru_cache
def get_settings() -> Settings:
    return Settings()
