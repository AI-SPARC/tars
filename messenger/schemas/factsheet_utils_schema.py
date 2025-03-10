from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class SupportEnum(str, Enum):
    SUPPORTED = "SUPPORTED"
    REQUIRED = "REQUIRED"
    
class ActionScopesEnum(str, Enum):
    INSTANT = "NODE"
    NODE = "NODE"
    EDGE = "EDGE"

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

class OptionalParameter(BaseModel):
    parameter: str = Field(..., description="Full name of optional parameter")
    support: SupportEnum = Field(..., description="Type of support for the optional parameter, the following values are possible: [SUPPORTED, REQUIRED]")
    description: str = Field(..., description="Free-form text: description of optional parameter")

class AgvAction(BaseModel):
    actionType: str = Field(..., description="Unique type of action corresponding to action.actionType.")
    actionDescription: SupportEnum = Field(..., description="Free-form text: description of the action.")
    actionScopes: List[ActionScopesEnum] = Field(..., description="Array of allowed scopes for using this action type. [INSTANT, NODE, EDGE]")