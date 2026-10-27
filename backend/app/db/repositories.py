
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import EvidenceItem, Incident
from app.schemas.evidence import EvidenceCreate
from app.schemas.incident import IncidentCreate, IncidentUpdate


def create_incident(db: Session, incident_data: IncidentCreate) -> Incident:
    incident = Incident(**incident_data.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


def get_incident(db: Session, incident_id: UUID) -> Optional[Incident]:
    statement = select(Incident).where(
        Incident.incident_id == incident_id
    )
    return db.execute(statement).scalar_one_or_none()


def list_incidents(db: Session, limit: int = 50, offset: int = 0) -> List[Incident]:
    statement = (
        select(Incident)
        .order_by(Incident.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.execute(statement).scalars().all())


def update_incident(
    db: Session,
    incident_id: UUID,
    incident_data: IncidentUpdate,
) -> Optional[Incident]:
    incident = get_incident(db, incident_id)

    if incident is None:
        return None

    updates = incident_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(incident, field, value)

    db.commit()
    db.refresh(incident)
    return incident


def create_evidence(
    db: Session,
    evidence_data: EvidenceCreate,
) -> EvidenceItem:
    evidence = EvidenceItem(**evidence_data.model_dump())
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    return evidence


def get_evidence(
    db: Session,
    evidence_id: UUID,
) -> Optional[EvidenceItem]:
    statement = select(EvidenceItem).where(
        EvidenceItem.evidence_id == evidence_id
    )
    return db.execute(statement).scalar_one_or_none()


def list_evidence_for_incident(
    db: Session,
    incident_id: UUID,
    limit: int = 100,
    offset: int = 0,
) -> List[EvidenceItem]:
    statement = (
        select(EvidenceItem)
        .where(EvidenceItem.incident_id == incident_id)
        .order_by(EvidenceItem.event_time.asc().nulls_last())
        .limit(limit)
        .offset(offset)
    )
    return list(db.execute(statement).scalars().all())
