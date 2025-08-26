from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    PROJECT_NAME: str = "SRFID Backend"
    PROJECT_DESCRIPTION: str = "A API REST para acesso dos recursos do sistema SmartRFID"
    PROJECT_VERSION: str = "0.0.1"
    POSTGRES_URL: str = "postgresql+psycopg://postgres:2411@localhost:5432/estoque"

    model_config: SettingsConfigDict = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


app_settings = AppSettings()
