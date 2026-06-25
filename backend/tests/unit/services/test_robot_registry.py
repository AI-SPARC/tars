import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base
from app.services.robot_registry import RobotRegistryService


@pytest.fixture
async def session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)
    async with maker() as db_session:
        yield db_session
    await engine.dispose()


async def test_get_or_create_robot_is_idempotent(session: AsyncSession) -> None:
    service = RobotRegistryService(session)

    first = await service.get_or_create("ResearchBot", "RB001")
    second = await service.get_or_create("ResearchBot", "RB001")

    assert first.id == second.id
    assert second.manufacturer == "ResearchBot"
    assert second.serial_number == "RB001"


async def test_update_connection_state_updates_last_seen(session: AsyncSession) -> None:
    service = RobotRegistryService(session)
    robot = await service.get_or_create("ResearchBot", "RB002")

    updated = await service.update_connection_state(robot.id, "ONLINE")

    assert updated.last_connection_state == "ONLINE"
    assert updated.last_seen_at is not None
