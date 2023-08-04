from os import environ

from pydantic_settings import BaseSettings, SettingsConfigDict


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    Usually, we have three environments: for development, testing and production.
    But in this situation, we only have standard settings for local development.
    """

    APP_HOST: str = environ.get("APP_HOST", "127.0.0.1")
    APP_PORT: int = int(environ.get("APP_PORT", 8000))

    LOG_FILE: str = environ.get("LOG_FILE", "operations.log")

    POSTGRES_DB: str = environ.get("POSTGRES_DB", "chat")
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_USER: str = environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PORT: int = int(environ.get("POSTGRES_PORT", 5432))
    POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "changeme")

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for async connection with database.
        """
        return "postgresql+psycopg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = DefaultSettings()
