from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Cipher API"
    APP_VERSION: str = "0.0.1"
    DEBUG: bool = False

    HOST: str = "localhost"
    PORT: int = 8000

    CORS_ORIGINS: list[str] = []

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
