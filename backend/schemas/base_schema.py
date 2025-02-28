from datetime import datetime
from pydantic import BaseModel

class BaseSchema(BaseModel):
    created_at: datetime
    updated_at: datetime
