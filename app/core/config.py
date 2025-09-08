from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    """Application settings"""

    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    POSTGRES_DB: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres_password"

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def database_url(self):
        user = f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
        database = f'{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}'
        return f'postgresql+asyncpg://{user}@{database}'

    @property
    def redis_url(self):
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}:{self.REDIS_PASSWORD}'
        


settings = Settings()