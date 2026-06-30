from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class RouteNode:
    node_id: str
    x: float
    y: float
    theta: float
    map_id: str
    allowed_deviation_xy: float = 0.1
    allowed_deviation_theta: float = 0.1
    description: str = ""


@dataclass(frozen=True)
class RouteEdge:
    edge_id: str
    start_node_id: str
    end_node_id: str
    description: str = ""


def build_order(
    *,
    manufacturer: str,
    serial_number: str,
    header_id: int,
    order_id: str,
    nodes: list[RouteNode],
    edges: list[RouteEdge],
    order_update_id: int = 0,
    protocol_version: str = "3.0.0",
    timestamp: datetime | None = None,
) -> dict[str, Any]:
    if not nodes:
        raise ValueError("A VDA 5050 order requires at least one node")
    if len(edges) != len(nodes) - 1:
        raise ValueError("A VDA 5050 order requires len(edges) == len(nodes) - 1")

    emitted_at = timestamp or datetime.now(UTC)
    payload: dict[str, Any] = {
        "headerId": header_id,
        "timestamp": _format_vda_timestamp(emitted_at),
        "version": protocol_version,
        "manufacturer": manufacturer,
        "serialNumber": serial_number,
        "orderId": order_id,
        "orderUpdateId": order_update_id,
        "nodes": [_node_payload(node, index * 2) for index, node in enumerate(nodes)],
        "edges": [_edge_payload(edge, index * 2 + 1) for index, edge in enumerate(edges)],
    }
    return payload


def _node_payload(node: RouteNode, sequence_id: int) -> dict[str, Any]:
    return {
        "nodeId": node.node_id,
        "sequenceId": sequence_id,
        "nodeDescription": node.description,
        "released": True,
        "nodePosition": {
            "x": node.x,
            "y": node.y,
            "theta": node.theta,
            "allowedDeviationXY": {
                "a": node.allowed_deviation_xy,
                "b": node.allowed_deviation_xy,
                "theta": 0.0,
            },
            "allowedDeviationTheta": node.allowed_deviation_theta,
            "mapId": node.map_id,
        },
        "actions": [],
    }


def _edge_payload(edge: RouteEdge, sequence_id: int) -> dict[str, Any]:
    return {
        "edgeId": edge.edge_id,
        "sequenceId": sequence_id,
        "edgeDescription": edge.description,
        "released": True,
        "startNodeId": edge.start_node_id,
        "endNodeId": edge.end_node_id,
        "actions": [],
    }


def _format_vda_timestamp(value: datetime) -> str:
    utc_value = value.astimezone(UTC)
    return utc_value.isoformat(timespec="milliseconds").replace("+00:00", "Z")
