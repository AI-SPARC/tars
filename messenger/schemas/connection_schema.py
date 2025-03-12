from pydantic import BaseModel, Field

from schemas.header_schema import Header

class Connection(BaseModel):
    header: Header
    connectionState: str = Field(..., description="Enum {'ONLINE', 'OFFLINE', 'CONNECTIONBROKEN'}")