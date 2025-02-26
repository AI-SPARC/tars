from datetime import datetime, UTC
from pydantic import BaseModel

class BaseSchema(BaseModel):
    created_at: datetime = datetime.now(UTC)
    updated_at: datetime = datetime.now(UTC)
