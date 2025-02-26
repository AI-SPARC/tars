from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    """
    
    API_NAME: str = "Fleet Manager"
    API_VERSION: str = "v1"
    API_DOCS: str = "/docs"
    API_REDOC : str = "/redoc"
    API_DEBUG: bool = False
    
    ENABLE_LOCAL_CORS : bool = True
    
    # "postgresql" ou "sqlite"
    DATABASE_TYPE: str = "sqlite"
    
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = 5432
    DB_NAME: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    SQLITE_PATH: Optional[str] = "./database.db"


    @property
    def database_url(self) -> str:
        """Build the database connection URL based on the selected database type."""
        if self.DATABASE_TYPE == "sqlite":
            return f"sqlite+aiosqlite:///{self.SQLITE_PATH}"
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # MQTT_BROKER: str
    # MQTT_PORT: int = 1883
    # MQTT_USERNAME: str | None = None
    # MQTT_PASSWORD: str | None = None
    # MQTT_KEEPALIVE: int = 60
    # MQTT_TOPIC_PREFIX: str = "fleet"

    # SECRET_KEY: str
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # class Config:
    #     env_file = ".env"

settings = Settings()
