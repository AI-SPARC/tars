from pydantic import BaseModel
from typing import List, Optional

from messenger.schemas.header_schema import Header

class Velocity(BaseModel):
    x: float
    y: float
    omega: float

class Position(BaseModel):
    x: float
    y: float
    theta: float
    mapId: str

class BatteryState(BaseModel):
    batteryCharge: float
    charging: bool

class SafetyState(BaseModel):
    eStop: str
    fieldViolation: bool

class Load(BaseModel):
    loadId: str
    loadType: str

class Error(BaseModel):
    errorType: str
    errorDescription: str
    errorLevel: str

class Information(BaseModel):
    informationType: str
    informationDescription: str

class AGVState(BaseModel):
    header: Header
    agvPosition: Position
    velocity: Velocity
    batteryState: BatteryState
    safetyState: SafetyState
    driving: bool
    paused: bool
    loads: List[Load]
    errors: List[Error]
    information: List[Information]
    orderId: str
    orderUpdateId: int
    lastNodeId: Optional[str] = None
    lastNodeSequenceId: Optional[int] = None