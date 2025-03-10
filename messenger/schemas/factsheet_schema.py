from pydantic import BaseModel, Field
from typing import List, Optional

from schemas.header_schema import Header
from schemas.factsheet_utils_schema import MaxStringLens, MaxArrayLens, Timing


class TypeSpecification(BaseModel):
    seriesName: str = Field(..., description="Free text generalized series name as specified by manufacturer.")
    seriesDescription: str = Field(..., description="Free text human-readable description of the AGV type series.")
    agvKinematic: str = Field(..., description="Simplified description of the AGV kinematics type: [DIFF, OMNI, THREEWHEEL]")
    agvClass: str = Field(..., description="Simplified description of the AGV class.[FORKLIFT, CONVEYOR, TUGGER, CARRIER]")
    maxLoadMass: float = Field(..., description="[kg], Maximum loadable mass.")
    localizationTypes: List[str] = Field(..., description="Simplified description of localization type.")
    navigationTypes: List[str] = Field(..., description="Array of path planning types supported by the AGV, sorted by priority.")

class PhysicalParameters(BaseModel):
    speedMin: float = Field(..., description="[m/s] Minimal controlled continuous speed of the AGV.")
    speedMax: float = Field(..., description="[m/s] Maximum speed of the AGV.")
    angularSpeedMin: float = Field(..., description="[Rad/s] Minimal controlled continuous rotation speed of the AGV.")
    angularSpeedMax: float = Field(..., description="[Rad/s] Maximum rotation speed of the AGV.")
    accelerationMax: float = Field(..., description="[m/s²] Maximum acceleration with maximum load.")
    decelerationMax: float = Field(..., description="[m/s²] Maximum deceleration with maximum load.")
    heightMin: float = Field(..., description="[m] Minimum height of the AGV.")
    heightMax: float = Field(..., description="[m] Maximum height of the AGV.")
    width: float = Field(..., description="[m] Width of the AGV.")
    length: float = Field(..., description="[m] Length of the AGV.")

class ProtocolLimits(BaseModel):
    maxStringLens : MaxStringLens
    maxArrayLens : MaxArrayLens
    timing :Timing

class ProtocolFeatures(BaseModel):
    optionalParameters : List[OptionalParameter]
    agvActions : List[AgvAction]
    actionParameters : List[ActionParameter]
    
class Navigation(BaseModel):
    navigationType: str = Field(..., description="Tipo de navegação utilizada pelo AGV.")
    speed: float = Field(..., description="Velocidade máxima do AGV em m/s.")

class Communication(BaseModel):
    interface: str = Field(..., description="Interface de comunicação utilizada pelo AGV.")
    protocol: str = Field(..., description="Protocolo de comunicação utilizado pelo AGV.")

class Factsheet(BaseModel):
    header: Header
    safety: Safety
    battery: Battery
    dimensions: Dimensions
    load: Load
    navigation: Navigation
    communication: Communication
    additionalInfo: Optional[str] = Field(None, description="Informações adicionais sobre o AGV.")
