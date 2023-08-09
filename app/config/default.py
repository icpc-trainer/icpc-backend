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

    ALLOW_ORIGINS: str = environ.get("ALLOW_ORIGINS", "")
    ALLOW_CREDENTIALS: bool = environ.get("ALLOW_CREDENTIALS", "False").lower() == "true"
    ALLOW_METHODS: str = environ.get("ALLOW_METHODS", "")
    ALLOW_HEADERS: str = environ.get("ALLOW_HEADERS", "")

    CONTEST_API_URL: str = environ.get(
        "CONTEST_API_URL", "https://api.contest.yandex.net/api/public/v2"
    )

    LOG_FILE: str = environ.get("LOG_FILE", "operations.log")

    POSTGRES_DB: str = environ.get("POSTGRES_DB", "icpc_db")
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_USER: str = environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PORT: int = int(environ.get("POSTGRES_PORT", 5432))
    POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "changeme")

    REDIS_HOST: str = environ.get("REDIS_HOST", "redis")
    REDIS_PORT: int = int(environ.get("REDIS_PORT", "6379"))

    MAX_CONNECTIONS_PER_GROUP: int = int(environ.get("MAX_CONNECTIONS_PER_GROUP", 3))

    @property
    def cors_settings(self) -> dict:
        return {
            "allow_origins": self.ALLOW_ORIGINS.split(","),
            "allow_credentials": self.ALLOW_CREDENTIALS,
            "allow_methods": self.ALLOW_METHODS.split(","),
            "allow_headers": self.ALLOW_HEADERS.split(","),
        }

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
