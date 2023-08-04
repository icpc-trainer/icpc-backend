from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
# TODO: remove next line
# from sqlalchemy.orm import sessionmaker

from app.config import settings


class SessionManager:
    """
    A class that implements the necessary functionality for working with the database:
    issuing sessions, storing and updating connection settings.
    """

    def __init__(self) -> None:
        self.refresh()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance  # noqa

    def get_session_maker(self) -> async_sessionmaker:
        return async_sessionmaker(self.engine, expire_on_commit=False)
        # TODO: remove next line
        # return async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    def refresh(self) -> None:
        self.engine = create_async_engine(settings.database_uri, echo=True, future=True)


async def get_session() -> AsyncSession:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        yield session


__all__ = [
    "get_session",
]
