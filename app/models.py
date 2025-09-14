import enum
import uuid
from sqlalchemy import (
    Column, String, Text, Enum, JSON, DateTime, MetaData, func
)
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class JobStatus(str, enum.Enum):
    enabled = "enabled"
    disabled = "disabled"

class ScheduleType(str, enum.Enum):
    cron = "cron"
    interval = "interval"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    schedule_type = Column(Enum(ScheduleType), nullable=False)
    schedule_expr = Column(String(255), nullable=False)
    timezone = Column(String(64), nullable=True, default="UTC")
    payload = Column(JSON, nullable=True)
    status = Column(Enum(JobStatus), nullable=False, default=JobStatus.enabled)
    last_run_at = Column(DateTime(timezone=True), nullable=True)
    next_run_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())