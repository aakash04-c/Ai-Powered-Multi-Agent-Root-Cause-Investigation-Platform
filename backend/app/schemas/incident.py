
from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


Severity = Literal["SEV1", "SEV2", "SEV3", "SEV4", "UNKNOWN"]
IncidentStatus = Literal["OPEN", "INVESTIGATING", "RESOLVED", "CLOSED"]


class IncidentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    original_text: str = Field(min_length=1)
    affected_service: Optional[str] = None
    severity: Severity = "UNKNOWN"
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None


class IncidentUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    original_text: Optional[str] = Field(default=None, min_length=1)
    affected_service: Optional[str] = None
    severity: Optional[Severity] = None
    status: Optional[IncidentStatus] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None


class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    incident_id: UUID
    title: str
    original_text: str
    affected_service: Optional[str]
    severity: Severity
    status: IncidentStatus
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
