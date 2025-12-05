from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    PROJECT_NAME: str = "SRFID Backend"
    PROJECT_DESCRIPTION: str = "A API REST para acesso dos recursos do sistema SmartRFID"
    PROJECT_VERSION: str = "0.0.1"

    ALLOWED_ORIGINS: list[str] = ["localhost:3000"]

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "2411"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "estoque"
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET: str
    JWT_ACCESS_EXIPIRE_MINUTES: int = 60  # Uma hora
    JWT_REFRESH_EXPIRE_DAYS: int = 7  # Uma semana

    model_config: SettingsConfigDict = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    @property
    def POSTGRES_URL(self) -> str:
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


app_settings = AppSettings()
