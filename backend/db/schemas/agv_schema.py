from schemas.base import BaseSchema

class AGVSchema(BaseSchema):
    agv_id: int
    manufacturer: str
    serial_number: str
