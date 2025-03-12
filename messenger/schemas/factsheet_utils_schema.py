from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

# ----------- Enums -----------
class SupportEnum(str, Enum):
    SUPPORTED = "SUPPORTED"
    REQUIRED = "REQUIRED"
    
class ActionScopesEnum(str, Enum):
    INSTANT = "INSTANT"
    NODE = "NODE"
    EDGE = "EDGE"
    
class ValueDataTypeEnum(str, Enum):
    BOOL = 'BOOL'
    NUMBER = 'NUMBER'
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'
    STRING = 'STRING'
    OBJECT = 'OBJECT'
    ARRAY = 'ARRAY'

class BlockingTypesEnum(str, Enum):
    NONE = 'NONE'
    SOFT = 'SOFT'
    HARD = 'HARD'

class TypeEnum(str, Enum):
    DRIVE = 'DRIVE'
    CASTER = 'CASTER'
    FIXED = 'FIXED'
    MECANUM = 'MECANUM'
    
# ----------- Utils -----------
class Position(BaseModel):
    x : float = Field(..., description="[m], x-position in AGV coordinate system.")
    y : float = Field(..., description="[m], y-position in AGV coordinate system.")
    theta : float = Field(..., description="[rad], orientation of the wheel in AGV coordinate system. Necessary for fixed wheels.")
    
class PolygonPoint(BaseModel):
    x : float = Field(..., description="[m], X-position of polygon point.")
    y : float = Field(..., description="[m], Y-position of polygon point.")

class LoadSet(BaseModel):
    setName : str = Field(..., description="Unique name of the load set, e.g., DEFAULT, SET1, etc.")
    loadType : str = Field(..., description="Type of load, e.g., EPAL, XLT1200, etc.")
    loadPositions : List[str] = Field(..., description="Array of load positions btw. load handling devices, this load set is valid for. If this parameter does not exist or is empty, this load set is valid for all load handling devices on this AGV.")	
    # boundingBoxReference	JSON object	Bounding box reference as defined in parameter loads[] in state message.
    # loadDimensions	JSON object	Load dimensions as defined in parameter loads[] in state message.
    maxWeight : float = Field(..., description="[kg], maximum weight of load type.")
    minLoadhandlingHeight: float  = Field(..., description="[m], minimum allowed height for handling of this load type and weight references to boundingBoxReference.")
    maxLoadhandlingHeight : float = Field(..., description="[m], maximum allowed height for handling of this load type and weight references to boundingBoxReference.")
    minLoadhandlingDepth : float = Field(..., description="[m], minimum allowed depth for this load type and weight references to boundingBoxReference.")
    maxLoadhandlingDepth : float = Field(..., description="[m], maximum allowed depth for this load type and weight references to boundingBoxReference.")
    minLoadhandlingTilt : float = Field(..., description="[rad], minimum allowed tilt for this load type and weight.")
    maxLoadhandlingTilt : float = Field(..., description="[rad], maximum allowed tilt for this load type and weight.")
    agvSpeedLimit : float = Field(..., description="[m/s], maximum allowed speed for this load type and weight.")
    agvAccelerationLimit : float = Field(..., description="[m/s²], maximum allowed acceleration for this load type and weight.")
    agvDecelerationLimit : float = Field(..., description="[m/s²], maximum allowed deceleration for this load type and weight.")
    pickTime : float = Field(..., description="[s], approx. time for picking up the load")
    dropTime : float = Field(..., description="[s], approx. time for dropping the load.")
    description : str = Field(..., description="Free-form text: description of the load handling set.")

class VersionInfo(BaseModel):
    key : str = Field(..., description="Key of the software/hardware version used. (e.g., softwareVersion)")
    value : str = Field(..., description="The version corresponding to the key. (e.g., v1.12.4-beta)")

class Network(BaseModel):
    dnsServers : List[str] = Field(..., description="Array of Domain Name Servers (DNS) used by the vehicle.")
    ntpServers : List[str] = Field(..., description="Array of Network Time Protocol (NTP) servers used by the vehicle.")
    localIpAddress : str = Field(..., description="A priori assigned IP address used to communicate with the MQTT broker. Note that this IP address should not be modified/changed during operations.")
    netmask : str = Field(..., description="The subnet mask used in the network configuration corresponding to the local IP address.")
    defaultGateway : str = Field(..., description="The default gateway used by the vehicle, corresponding to the local IP address.")

# ----------- Protocol Limits -----------
class MaxStringLens(BaseModel):
    msgLen: int = Field(..., description="Maximum MQTT message length.")
    topicSerialLen: int = Field(..., description="Maximum length of serial number part in MQTT-topics.")
    topicElemLen: int = Field(..., description="Maximum length of all other parts in MQTT topics.")
    idLen: int = Field(..., description="Maximum length of ID strings.")
    idNumericalOnly: bool = Field(..., description="If true ID strings need to contain numerical values only.")
    enumLen: int = Field(..., description="Maximum length of enum and key strings.")
    loadIdLen: int = Field(..., description="Maximum length of loadId strings.")

class MaxArrayLens(BaseModel):
    order_nodes: int = Field(..., description="Maximum number of nodes per order processable by the AGV.")
    order_edges: int = Field(..., description="Maximum number of edges per order processable by the AGV.")
    node_actions: int = Field(..., description="Maximum number of actions per node processable by the AGV.")
    edge_actions: int = Field(..., description="Maximum number of actions per edge processable by the AGV.")
    actions_actionsParameters: int = Field(..., description="Maximum number of parameters per action processable by the AGV.")
    instantActions: int = Field(..., description="Maximum number of instant actions per message processable by the AGV.")
    trajectory_knotVector: int = Field(..., description="Maximum number of knots per trajectory processable by the AGV.")
    trajectory_controlPoints: int = Field(..., description="Maximum number of control points per trajectory processable by the AGV.")
    state_nodeStates: int = Field(..., description="Maximum number of nodeStates sent by the AGV, maximum number of nodes in base of AGV.")
    state_edgeStates: int = Field(..., description="Maximum number of edgeStates sent by the AGV, maximum number of edges in base of AGV.")
    state_loads: int = Field(..., description="Maximum number of load objects sent by the AGV.")
    state_actionStates: int = Field(..., description="Maximum number of actionStates sent by the AGV.")
    state_errors: int = Field(..., description="Maximum number of errors sent by the AGV in one state message.")
    state_information: int = Field(..., description="Maximum number of information sent by the AGV in one state message.")
    error_errorReferences: int = Field(..., description="Maximum number of error references sent by the AGV for each error.")
    information_infoReferences: int = Field(..., description="Maximum number of info references sent by the AGV for each information.")


class Timing(BaseModel):
    minOrderInterval: float = Field(..., description="[s], Minimum interval sending order messages to the AGV.")
    minStateInterval: float = Field(..., description="[s], Minimum interval for sending state messages.")
    defaultStateInterval: float = Field(..., description="[s], Default interval for sending state messages, if not defined, the default value from the main document is used.")
    visualizationInterval: float = Field(..., description="[s], Default interval for sending messages on visualization topic.")

# ----------- Protocol Features -----------
class OptionalParameter(BaseModel):
    parameter: str = Field(..., description="Full name of optional parameter")
    support: SupportEnum = Field(..., description="Type of support for the optional parameter, the following values are possible: [SUPPORTED, REQUIRED]")
    description: str = Field(..., description="Free-form text: description of optional parameter")

class AgvAction(BaseModel):
    actionType: str = Field(..., description="Unique type of action corresponding to action.actionType.")
    actionDescription: SupportEnum = Field(..., description="Free-form text: description of the action.")
    actionScopes: List[ActionScopesEnum] = Field(..., description="Array of allowed scopes for using this action type. [INSTANT, NODE, EDGE]")

class ActionParameter(BaseModel):
    key: str = Field(..., description="Key string for parameter.")
    valueDataType: ValueDataTypeEnum = Field(..., description="Data type of value, possible data types are: 'BOOL', 'NUMBER', 'INTEGER', 'FLOAT', 'STRING', 'OBJECT', 'ARRAY'.")
    description: str = Field(..., description="Free-form text: description of the parameter.")
    isOptional:	bool = Field(..., description="true: optional parameter.")

# ----------- AGV Geometry -----------
class WheelDefinition(BaseModel):
    type_: TypeEnum = Field(..., alias="type", description="Wheel typeEnum {'DRIVE', 'CASTER', 'FIXED', 'MECANUM'}.")	
    isActiveDriven : bool = Field(..., description="true: wheel is actively driven.")
    isActiveSteered	: bool = Field(..., description="true: wheel is actively steered.")
    position : Position
    diameter : float = Field(..., description="[m], nominal diameter of wheel.")
    width : float = Field(..., description="[m], nominal width of wheel.")
    centerDisplacement : float = Field(..., description="[m], nominal displacement of the wheel's center to the rotation point (necessary for caster wheels). If the parameter is not defined, it is assumed to be 0.")
    constraints : str = Field(..., description="Free-form text: can be used by the manufacturer to define constraints.")
    
    class Config:
        populate_by_name = True 
    
class Envelope2d(BaseModel):
    set_ : str = Field(..., alias="set", description="Name of the envelope curve set.")
    polygonPoints : List[PolygonPoint]
    description: str = Field(..., description="Free-form text: description of envelope curve set.")
    class Config:
        populate_by_name = True 
        
class Envelope3d(BaseModel):
    set_ : str = Field(..., alias="set", description="Name of the envelope curve set.")
    format_	: str = Field(..., alias="format", description="Format of data, e.g., DXF.")
    # data	JSON object	3D-envelope curve data, format specified in 'format'.
    url : str = Field(..., description="Protocol and URL definition for downloading the 3D-envelope curve data, e.g., ftp://xxx.yyy.com/ac4dgvhoif5tghji.")
    description: str = Field(..., description="Free-form text: description of envelope curve set.")