from pydantic import BaseModel, Field


class RobotCreate(BaseModel):
    manufacturer: str
    serial_number: str = Field(alias="serialNumber")
    display_name: str | None = Field(default=None, alias="displayName")


class RobotRead(BaseModel):
    id: str
    manufacturer: str
    serial_number: str = Field(serialization_alias="serialNumber")
    display_name: str | None = Field(serialization_alias="displayName")
    protocol_version: str = Field(serialization_alias="protocolVersion")
    last_connection_state: str = Field(serialization_alias="lastConnectionState")


class RobotStateRead(BaseModel):
    id: str
    robot_id: str = Field(serialization_alias="robotId")
    header_id: int | None = Field(serialization_alias="headerId")
    order_id: str | None = Field(serialization_alias="orderId")
    order_update_id: int | None = Field(serialization_alias="orderUpdateId")
    last_node_id: str | None = Field(serialization_alias="lastNodeId")
    last_node_sequence_id: int | None = Field(serialization_alias="lastNodeSequenceId")
    battery_charge: float | None = Field(serialization_alias="batteryCharge")
    operating_mode: str | None = Field(serialization_alias="operatingMode")
    errors: list[dict] | None
    safety_state: dict | None = Field(serialization_alias="safetyState")
    agv_position: dict | None = Field(serialization_alias="agvPosition")
    node_states: list[dict] | None = Field(serialization_alias="nodeStates")
    edge_states: list[dict] | None = Field(serialization_alias="edgeStates")
    action_states: list[dict] | None = Field(serialization_alias="actionStates")
    raw_payload: dict = Field(serialization_alias="rawPayload")


class MapCreate(BaseModel):
    name: str
    description: str | None = None


class MapRead(BaseModel):
    id: str
    name: str
    description: str | None


class NodeCreate(BaseModel):
    node_key: str = Field(alias="nodeKey")
    x: float
    y: float
    theta: float = 0.0


class EdgeCreate(BaseModel):
    edge_key: str = Field(alias="edgeKey")
    from_node_key: str = Field(alias="fromNodeKey")
    to_node_key: str = Field(alias="toNodeKey")
    distance: float = 1.0
    bidirectional: bool = False


class RoutePreviewRequest(BaseModel):
    start_node_key: str = Field(alias="startNodeKey")
    goal_node_key: str = Field(alias="goalNodeKey")


class RoutePreviewRead(BaseModel):
    node_keys: list[str] = Field(serialization_alias="nodeKeys")


class MissionCreate(BaseModel):
    assigned_robot_id: str | None = Field(default=None, alias="assignedRobotId")
    start_node_key: str = Field(alias="startNodeKey")
    goal_node_key: str = Field(alias="goalNodeKey")
    priority: int = 0


class MissionRead(BaseModel):
    id: str
    assigned_robot_id: str | None = Field(serialization_alias="assignedRobotId")
    start_node_key: str = Field(serialization_alias="startNodeKey")
    goal_node_key: str = Field(serialization_alias="goalNodeKey")
    status: str
    priority: int
