from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Cipher API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    CORS_ORIGINS: list[str] = ["*"]

    ENV: str = "development"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
