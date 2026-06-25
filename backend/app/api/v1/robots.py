from fastapi import APIRouter, status
from sqlalchemy import select

from app.api.deps import SessionDep
from app.api.v1.schemas import RobotCreate, RobotRead
from app.db.base import Robot
from app.services.robot_registry import RobotRegistryService

router = APIRouter(prefix="/robots", tags=["robots"])


@router.get("", response_model=list[RobotRead])
async def list_robots(session: SessionDep) -> list[Robot]:
    result = await session.execute(select(Robot).order_by(Robot.created_at))
    return list(result.scalars())


@router.post("", response_model=RobotRead, status_code=status.HTTP_201_CREATED)
async def create_robot(payload: RobotCreate, session: SessionDep) -> Robot:
    return await RobotRegistryService(session).get_or_create(
        payload.manufacturer, payload.serial_number, payload.display_name
    )
