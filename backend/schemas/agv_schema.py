from pydantic import BaseModel
from schemas.base_schema import BaseSchema

class AGVCreate(BaseModel):
    """Schema for creating a new AGV."""
    manufacturer: str
    serial_number: str

class AGVRead(BaseSchema):
    """Schema for reading AGV data, including database-generated fields."""
    id: str
    manufacturer: str
    serial_number: str

    class Config:
        from_attributes = True
