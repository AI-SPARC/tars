from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime

from messenger.schemas.header_schema import Header

class ActionParameter(BaseModel):
    key: str
    value: Union[List[str], bool, float, str, dict]

class Action(BaseModel):
    actionId: str
    actionType: str
    blockingType: str
    actionDescription: Optional[str] = None
    actionParameters: Optional[List[ActionParameter]] = []

class NodePosition(BaseModel):
    x: float
    y: float
    mapId: str
    theta: Optional[float] = None
    allowedDeviationXY: Optional[float] = None
    allowedDeviationTheta: Optional[float] = None
    mapDescription: Optional[str] = None

class Node(BaseModel):
    nodeId: str
    sequenceId: int = Field(ge=0)
    released: bool
    nodeDescription: Optional[str] = None
    nodePosition: Optional[NodePosition] = None
    actions: List[Action] = []

class ControlPoint(BaseModel):
    x: float
    y: float
    weight: Optional[float] = 1.0

class Trajectory(BaseModel):
    degree: int = Field(ge=1)
    knotVector: List[float]
    controlPoints: List[ControlPoint]

class Corridor(BaseModel):
    leftWidth: float = Field(ge=0.0)
    rightWidth: float = Field(ge=0.0)
    corridorRefPoint: Optional[str] = None

class Edge(BaseModel):
    edgeId: str
    sequenceId: int = Field(ge=0)
    released: bool
    startNodeId: str
    endNodeId: str
    edgeDescription: Optional[str] = None
    maxSpeed: Optional[float] = None
    maxHeight: Optional[float] = None
    minHeight: Optional[float] = None
    orientation: Optional[float] = None
    orientationType: Optional[str] = "TANGENTIAL"
    direction: Optional[str] = None
    rotationAllowed: Optional[bool] = None
    maxRotationSpeed: Optional[float] = None
    length: Optional[float] = None
    trajectory: Optional[Trajectory] = None
    corridor: Optional[Corridor] = None
    actions: List[Action] = []

class OrderMessage(BaseModel):
    header : Header
    orderId: str
    orderUpdateId: int = Field(ge=0)
    zoneSetId: Optional[str] = None
    nodes: List[Node]
    edges: List[Edge]
