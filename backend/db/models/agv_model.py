from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, UTC
from core.base import Base

class AGVModel(Base):
    __tablename__ = "agvs"

    id = Column(Integer, primary_key=True, index=True)
    manufacturer = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
