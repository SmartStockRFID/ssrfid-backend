from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    POSTGRES_URL: str = "postgresql+psycopg://postgres:2411@localhost:5432/estoque"

    model_config: SettingsConfigDict = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


app_settings = AppSettings()
