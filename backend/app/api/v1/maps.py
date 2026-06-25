from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import SessionDep
from app.api.v1.schemas import (
    EdgeCreate,
    MapCreate,
    MapRead,
    NodeCreate,
    RoutePreviewRead,
    RoutePreviewRequest,
)
from app.db.base import MapLayout
from app.services.map_service import MapService

router = APIRouter(prefix="/maps", tags=["maps"])


@router.get("", response_model=list[MapRead])
async def list_maps(session: SessionDep) -> list[MapLayout]:
    result = await session.execute(select(MapLayout).order_by(MapLayout.name))
    return list(result.scalars())


@router.post("", response_model=MapRead, status_code=status.HTTP_201_CREATED)
async def create_map(payload: MapCreate, session: SessionDep) -> MapLayout:
    return await MapService(session).create_map(payload.name, payload.description)


@router.post("/{map_id}/nodes", status_code=status.HTTP_201_CREATED)
async def add_node(map_id: str, payload: NodeCreate, session: SessionDep) -> dict[str, str]:
    node = await MapService(session).add_node(
        map_id, payload.node_key, payload.x, payload.y, payload.theta
    )
    return {"id": node.id, "nodeKey": node.node_key}


@router.post("/{map_id}/edges", status_code=status.HTTP_201_CREATED)
async def add_edge(map_id: str, payload: EdgeCreate, session: SessionDep) -> dict[str, str]:
    edge = await MapService(session).add_edge(
        map_id,
        payload.edge_key,
        payload.from_node_key,
        payload.to_node_key,
        payload.distance,
        payload.bidirectional,
    )
    return {"id": edge.id, "edgeKey": edge.edge_key}


@router.post("/{map_id}/route-preview", response_model=RoutePreviewRead)
async def route_preview(
    map_id: str, payload: RoutePreviewRequest, session: SessionDep
) -> RoutePreviewRead:
    try:
        node_keys = await MapService(session).route_preview(
            map_id, payload.start_node_key, payload.goal_node_key
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return RoutePreviewRead(node_keys=node_keys)
