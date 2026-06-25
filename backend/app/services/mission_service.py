from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Mission


class MissionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_mission(
        self,
        start_node_key: str,
        goal_node_key: str,
        assigned_robot_id: str | None = None,
        priority: int = 0,
    ) -> Mission:
        mission = Mission(
            assigned_robot_id=assigned_robot_id,
            start_node_key=start_node_key,
            goal_node_key=goal_node_key,
            priority=priority,
            status="queued",
        )
        self.session.add(mission)
        await self.session.commit()
        await self.session.refresh(mission)
        return mission
