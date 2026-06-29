from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import MapLayout, MapNode, Mission, Robot
from app.services.event_bus import EventBus, get_event_bus


class MissionService:
    def __init__(self, session: AsyncSession, event_bus: EventBus | None = None) -> None:
        self.session = session
        self.event_bus = event_bus or get_event_bus()

    async def create_mission(
        self,
        map_id: str,
        start_node_key: str,
        goal_node_key: str,
        assigned_robot_id: str | None = None,
        priority: int = 0,
    ) -> Mission:
        if await self.session.get(MapLayout, map_id) is None:
            raise ValueError("Map not found")
        node_keys = set(
            (
                await self.session.execute(
                    select(MapNode.node_key).where(
                        MapNode.map_id == map_id,
                        MapNode.node_key.in_([start_node_key, goal_node_key]),
                    )
                )
            ).scalars()
        )
        missing_nodes = {start_node_key, goal_node_key} - node_keys
        if missing_nodes:
            raise ValueError(f"Map nodes not found: {', '.join(sorted(missing_nodes))}")
        if (
            assigned_robot_id is not None
            and await self.session.get(Robot, assigned_robot_id) is None
        ):
            raise ValueError("Assigned robot not found")

        mission = Mission(
            map_id=map_id,
            assigned_robot_id=assigned_robot_id,
            start_node_key=start_node_key,
            goal_node_key=goal_node_key,
            priority=priority,
            status="assigned" if assigned_robot_id is not None else "queued",
        )
        self.session.add(mission)
        await self.session.commit()
        await self.session.refresh(mission)
        self.event_bus.publish(
            "mission.created",
            robot_id=mission.assigned_robot_id,
            mission_id=mission.id,
            payload={"status": mission.status, "mapId": mission.map_id},
        )
        if mission.assigned_robot_id is not None:
            self.event_bus.publish(
                "mission.assigned",
                robot_id=mission.assigned_robot_id,
                mission_id=mission.id,
                payload={"status": mission.status},
            )
        return mission
