from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings"""


    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_CHANNEL: str = "image_channel"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()