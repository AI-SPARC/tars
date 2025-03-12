from pydantic import BaseModel, Field
from typing import List, Union, Any
from enum import Enum

from messenger.schemas.header_schema import Header

class BlockingType(str, Enum):
    NONE = "NONE"
    SOFT = "SOFT"
    HARD = "HARD"

class ActionParameter(BaseModel):
    key: str = Field(..., description="The key of the action parameter.")
    value: Union[List[Any], bool, float, int, str, dict] = Field(..., description="The value of the action parameter.")

class Action(BaseModel):
    actionId: str = Field(..., description="Unique ID to identify the action and map them to the actionState.")
    actionType: str = Field(..., description="Name of action as described in the first column of 'Actions and Parameters'.")
    actionDescription: str | None = Field(None, description="Additional information on the action.")
    blockingType: BlockingType = Field(..., description="Regulates execution constraints for the action.")
    actionParameters: List[ActionParameter] | None = Field(None, description="Array of actionParameter-objects for the indicated action.")

class InstantActions(BaseModel):
    header: Header
    actions: List[Action] = Field(..., description="List of actions the AGV should execute instantly.")
