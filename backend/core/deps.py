from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import SessionLocal

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting a database session."""
    async with SessionLocal() as session:
        yield session
