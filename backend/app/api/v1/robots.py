from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import SessionDep
from app.api.v1.schemas import RobotCreate, RobotRead, RobotStateRead
from app.db.base import Robot, RobotStateSnapshot
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


@router.get("/{robot_id}", response_model=RobotRead)
async def get_robot(robot_id: str, session: SessionDep) -> Robot:
    robot = await session.get(Robot, robot_id)
    if robot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found")
    return robot


@router.get("/{robot_id}/state/latest", response_model=RobotStateRead)
async def get_latest_robot_state(robot_id: str, session: SessionDep) -> RobotStateSnapshot:
    await _ensure_robot_exists(robot_id, session)
    latest = await RobotRegistryService(session).get_latest_state(robot_id)
    if latest is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Robot state not found")
    return latest


@router.get("/{robot_id}/states", response_model=list[RobotStateRead])
async def list_robot_states(robot_id: str, session: SessionDep) -> list[RobotStateSnapshot]:
    await _ensure_robot_exists(robot_id, session)
    result = await session.execute(
        select(RobotStateSnapshot)
        .where(RobotStateSnapshot.robot_id == robot_id)
        .order_by(RobotStateSnapshot.received_at.desc())
    )
    return list(result.scalars())


@router.get("/{robot_id}/factsheet")
async def get_robot_factsheet(robot_id: str, session: SessionDep) -> dict[str, Any]:
    robot = await _ensure_robot_exists(robot_id, session)
    if robot.factsheet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Robot factsheet not found"
        )
    return robot.factsheet


async def _ensure_robot_exists(robot_id: str, session: SessionDep) -> Robot:
    robot = await session.get(Robot, robot_id)
    if robot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found")
    return robot
