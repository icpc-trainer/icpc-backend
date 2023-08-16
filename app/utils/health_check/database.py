import redis
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings


async def health_check_db(session: AsyncSession) -> bool:
    health_check_query = select(text("1"))
    result = await session.scalars(health_check_query)
    return result is not None


async def health_check_redis() -> bool:
    try:
        r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
        )
        r.ping()
        return True
    except Exception:
        return False
