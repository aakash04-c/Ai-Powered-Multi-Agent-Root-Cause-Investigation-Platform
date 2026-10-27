from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import repositories
from app.schemas.evidence import EvidenceCreate, EvidenceResponse

router = APIRouter(prefix="/incidents", tags=["Evidence"])


@router.post(
    "/{incident_id}/evidence",
    response_model=EvidenceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest evidence for an incident",
)
def add_evidence(
    incident_id: UUID,
    payload: EvidenceCreate,
    db: Session = Depends(get_db),
) -> EvidenceResponse:
    incident = repositories.get_incident(db, incident_id)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot associate evidence: Incident '{incident_id}' not found",
        )

    payload.incident_id = incident_id
    return repositories.create_evidence(db, payload)


@router.get(
    "/{incident_id}/evidence",
    response_model=List[EvidenceResponse],
    status_code=status.HTTP_200_OK,
    summary="List evidence associated with an incident",
)
def list_evidence(
    incident_id: UUID,
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> List[EvidenceResponse]:
    incident = repositories.get_incident(db, incident_id)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident '{incident_id}' not found",
        )
    return repositories.list_evidence_for_incident(
        db, incident_id, limit=limit, offset=offset
    )
