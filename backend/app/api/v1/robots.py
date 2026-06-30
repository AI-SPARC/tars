from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.api.deps import EventBusDep, SessionDep
from app.api.v1.schemas import (
    InstantActionCreate,
    InstantActionRead,
    RobotCreate,
    RobotRead,
    RobotStateRead,
)
from app.db.base import Robot, RobotStateSnapshot
from app.mqtt.outbound import MqttPublisher, get_mqtt_publisher
from app.services.instant_action_service import InstantActionService
from app.services.robot_registry import RobotRegistryService

router = APIRouter(prefix="/robots", tags=["robots"])
PublisherDep = Annotated[MqttPublisher, Depends(get_mqtt_publisher)]


@router.get("", response_model=list[RobotRead])
async def list_robots(session: SessionDep) -> list[Robot]:
    result = await session.execute(select(Robot).order_by(Robot.created_at))
    return list(result.scalars())


@router.post("", response_model=RobotRead, status_code=status.HTTP_201_CREATED)
async def create_robot(payload: RobotCreate, session: SessionDep, event_bus: EventBusDep) -> Robot:
    return await RobotRegistryService(session, event_bus).get_or_create(
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


@router.post(
    "/{robot_id}/instant-actions",
    response_model=InstantActionRead,
    status_code=status.HTTP_202_ACCEPTED,
)
async def send_instant_action(
    robot_id: str,
    payload: InstantActionCreate,
    session: SessionDep,
    publisher: PublisherDep,
    event_bus: EventBusDep,
) -> InstantActionRead:
    result = await InstantActionService(session, publisher, event_bus).send(
        robot_id, payload.action_type, payload.action_parameters
    )
    if not result.accepted:
        status_code = status.HTTP_404_NOT_FOUND if result.errors == ["Robot not found"] else 400
        raise HTTPException(status_code=status_code, detail=result.errors)
    return InstantActionRead(
        accepted=True,
        topic=result.topic,
        payload=result.payload,
        errors=[],
    )


async def _ensure_robot_exists(robot_id: str, session: SessionDep) -> Robot:
    robot = await session.get(Robot, robot_id)
    if robot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found")
    return robot
