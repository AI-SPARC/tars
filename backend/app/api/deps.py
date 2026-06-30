from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db_session
from app.services.event_bus import EventBus, get_event_bus


async def get_session() -> AsyncGenerator[AsyncSession]:
    async for session in get_db_session():
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
EventBusDep = Annotated[EventBus, Depends(get_event_bus)]
