from typing import Annotated, Literal

from fastapi import APIRouter, Query
from sqlalchemy import func, select

from app.api.deps import SessionDep
from app.api.v1.schemas import MqttMessagePage, MqttMessageRead
from app.db.base import MqttMessageLog

router = APIRouter(prefix="/mqtt", tags=["mqtt"])


@router.get("/messages", response_model=MqttMessagePage)
async def list_mqtt_messages(
    session: SessionDep,
    direction: Annotated[Literal["inbound", "outbound"] | None, Query()] = None,
    message_type: Annotated[str | None, Query(alias="messageType")] = None,
    robot_id: Annotated[str | None, Query(alias="robotId")] = None,
    schema_valid: Annotated[bool | None, Query(alias="schemaValid")] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(alias="pageSize", ge=1, le=100)] = 50,
) -> MqttMessagePage:
    filters = []
    if direction is not None:
        filters.append(MqttMessageLog.direction == direction)
    if message_type is not None:
        filters.append(MqttMessageLog.message_type == message_type)
    if robot_id is not None:
        filters.append(MqttMessageLog.robot_id == robot_id)
    if schema_valid is not None:
        filters.append(MqttMessageLog.schema_valid == schema_valid)

    total = await session.scalar(
        select(func.count()).select_from(MqttMessageLog).where(*filters)
    )
    total = total or 0
    messages = list(
        (
            await session.execute(
                select(MqttMessageLog)
                .where(*filters)
                .order_by(MqttMessageLog.created_at.desc(), MqttMessageLog.id.desc())
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
        ).scalars()
    )
    pages = (total + page_size - 1) // page_size
    return MqttMessagePage(
        items=[MqttMessageRead.model_validate(message) for message in messages],
        page=page,
        page_size=page_size,
        total=total,
        pages=pages,
    )
