from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession


async def health_check_db(session: AsyncSession) -> bool:
    health_check_query = select(text("1"))
    result = await session.scalars(health_check_query)
    return result is not None
