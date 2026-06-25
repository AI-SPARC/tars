from fastapi import APIRouter, status
from sqlalchemy import select

from app.api.deps import SessionDep
from app.api.v1.schemas import MissionCreate, MissionRead
from app.db.base import Mission
from app.services.mission_service import MissionService

router = APIRouter(prefix="/missions", tags=["missions"])


@router.get("", response_model=list[MissionRead])
async def list_missions(session: SessionDep) -> list[Mission]:
    result = await session.execute(select(Mission).order_by(Mission.created_at))
    return list(result.scalars())


@router.post("", response_model=MissionRead, status_code=status.HTTP_201_CREATED)
async def create_mission(payload: MissionCreate, session: SessionDep) -> Mission:
    return await MissionService(session).create_mission(
        payload.start_node_key,
        payload.goal_node_key,
        payload.assigned_robot_id,
        payload.priority,
    )
