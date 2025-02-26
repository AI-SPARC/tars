from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
import uuid

from core.base import Base

class AGVModel(Base):
    __tablename__ = "agvs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    manufacturer = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())