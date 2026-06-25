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
    last_connection_state: str = Field(serialization_alias="lastConnectionState")


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
