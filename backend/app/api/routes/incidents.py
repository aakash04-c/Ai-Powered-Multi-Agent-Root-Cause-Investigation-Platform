from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import repositories
from app.schemas.incident import IncidentCreate, IncidentResponse

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.post(
    "",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new incident",
)
def create_incident(
    payload: IncidentCreate,
    db: Session = Depends(get_db),
) -> IncidentResponse:
    return repositories.create_incident(db, payload)


@router.get(
    "",
    response_model=List[IncidentResponse],
    status_code=status.HTTP_200_OK,
    summary="List all tracked incidents",
)
def list_incidents(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> List[IncidentResponse]:
    return repositories.list_incidents(db, limit=limit, offset=offset)


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve incident details",
)
def get_incident(
    incident_id: UUID,
    db: Session = Depends(get_db),
) -> IncidentResponse:
    incident = repositories.get_incident(db, incident_id)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident '{incident_id}' not found",
        )
    return incident
