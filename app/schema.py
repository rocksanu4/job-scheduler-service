from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from enum import Enum
from uuid import UUID
from datetime import datetime

class ScheduleType(str, Enum):
    cron = "cron"
    interval = "interval"

class JobStatus(str, Enum):
    enabled = "enabled"
    disabled = "disabled"

class JobCreate(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str]
    schedule_type: ScheduleType
    schedule_expr: str
    timezone: Optional[str] = "IST"
    payload: Optional[Any] = None

class JobRead(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    schedule_type: ScheduleType
    schedule_expr: str
    timezone: Optional[str]
    payload: Optional[Any]
    status: JobStatus
    last_run_at: Optional[datetime]
    next_run_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
