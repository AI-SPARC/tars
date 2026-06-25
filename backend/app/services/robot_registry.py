from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Robot


class RobotRegistryService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_or_create(
        self, manufacturer: str, serial_number: str, display_name: str | None = None
    ) -> Robot:
        result = await self.session.execute(
            select(Robot).where(
                Robot.manufacturer == manufacturer,
                Robot.serial_number == serial_number,
            )
        )
        robot = result.scalar_one_or_none()
        if robot is not None:
            if display_name and robot.display_name != display_name:
                robot.display_name = display_name
                await self.session.commit()
                await self.session.refresh(robot)
            return robot

        robot = Robot(
            manufacturer=manufacturer,
            serial_number=serial_number,
            display_name=display_name,
            last_seen_at=datetime.now(UTC),
        )
        self.session.add(robot)
        await self.session.commit()
        await self.session.refresh(robot)
        return robot

    async def update_connection_state(self, robot_id: str, state: str) -> Robot:
        robot = await self.session.get(Robot, robot_id)
        if robot is None:
            raise ValueError(f"Robot not found: {robot_id}")
        robot.last_connection_state = state
        robot.last_seen_at = datetime.now(UTC)
        await self.session.commit()
        await self.session.refresh(robot)
        return robot
