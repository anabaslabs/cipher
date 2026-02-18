from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "CNS Solver API"
    APP_VERSION: str = "0.0.1"
    DEBUG: bool = False

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
