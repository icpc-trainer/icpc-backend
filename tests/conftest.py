from os import environ
from types import SimpleNamespace
from uuid import uuid4

import pytest
from alembic.config import Config
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from tests.utils import make_alembic_config

from app.config import settings
from app.db.models.base import BaseTable as Base


@pytest.fixture()
def postgres() -> str:
    tmp_name = ".".join([uuid4().hex, "pytest"])
    settings.POSTGRES_DB = tmp_name
    environ["POSTGRES_DB"] = tmp_name

    tmp_url = settings.database_uri
    if not database_exists(tmp_url):
        create_database(tmp_url)

    try:
        yield settings.database_uri
    finally:
        drop_database(tmp_url)


@pytest.fixture
def alembic_config(postgres: str) -> Config:
    """
    Создает файл конфигурации для alembic.
    """
    cmd_options = SimpleNamespace(
        config="app/db/", name="alembic", pg_url=postgres, raiseerr=False, x=None
    )
    return make_alembic_config(cmd_options)


@pytest.fixture
async def engine_async(postgres: str) -> AsyncEngine:
    engine = create_async_engine(postgres, future=True)
    yield engine
    await engine.dispose()


async def init_models(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture()
async def migrated_postgres(postgres, engine_async):
    await init_models(engine_async)


@pytest.fixture()
def session_maker(migrated_postgres, engine_async):
    session_maker = sessionmaker(engine_async, class_=AsyncSession, expire_on_commit=False)
    yield session_maker


@pytest.fixture()
async def session(session_maker):
    async with session_maker() as session:
        yield session
