from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from messenger.schemas.header_schema import Header

class AGVPosition(BaseModel):
    x: float
    y: float
    theta: float
    map_id: str = Field(..., alias="mapId")
    position_initialized: bool = Field(..., alias="positionInitialized")
    localization_score: Optional[float] = Field(None, ge=0.0, le=1.0, alias="localizationScore")
    deviation_range: Optional[float] = Field(None, alias="deviationRange")

class Velocity(BaseModel):
    vx: Optional[float] = None
    vy: Optional[float] = None
    omega: Optional[float] = None

class Visualization(BaseModel):
    header : Header
    serial_number: Optional[str] = Field(None, alias="serialNumber")
    agv_position: Optional[AGVPosition] = Field(None, alias="agvPosition")
    velocity: Optional[Velocity] = None
