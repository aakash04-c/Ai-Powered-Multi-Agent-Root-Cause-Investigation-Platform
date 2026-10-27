
import pytest

from app.db.database import SessionLocal
from app.db.models import EvidenceItem, Incident
from app.db.repositories import (
    create_evidence,
    create_incident,
    get_evidence,
    get_incident,
    list_evidence_for_incident,
    list_incidents,
    update_incident,
)
from app.schemas.evidence import EvidenceCreate
from app.schemas.incident import IncidentCreate, IncidentUpdate


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        # Remove records created by this test session.
        session.query(EvidenceItem).filter(
            EvidenceItem.incident_id.in_(
                session.query(Incident.incident_id).filter(
                    Incident.title.like("pytest repository test%")
                )
            )
        ).delete(synchronize_session=False)

        session.query(Incident).filter(
            Incident.title.like("pytest repository test%")
        ).delete(synchronize_session=False)

        session.commit()
        session.close()


def test_create_and_get_incident(db):
    incident = create_incident(
        db,
        IncidentCreate(
            title="pytest repository test - create",
            original_text="Checkout gateway returns 503",
            severity="SEV2",
        ),
    )

    found = get_incident(db, incident.incident_id)

    assert found is not None
    assert found.title == "pytest repository test - create"
    assert found.severity == "SEV2"


def test_list_incidents(db):
    incident = create_incident(
        db,
        IncidentCreate(
            title="pytest repository test - list",
            original_text="Test incident for listing",
        ),
    )

    results = list_incidents(db, limit=100)

    assert any(item.incident_id == incident.incident_id for item in results)


def test_update_incident(db):
    incident = create_incident(
        db,
        IncidentCreate(
            title="pytest repository test - update",
            original_text="Test incident for updating",
        ),
    )

    updated = update_incident(
        db,
        incident.incident_id,
        IncidentUpdate(status="INVESTIGATING"),
    )

    assert updated is not None
    assert updated.status == "INVESTIGATING"


def test_create_and_get_evidence(db):
    incident = create_incident(
        db,
        IncidentCreate(
            title="pytest repository test - evidence",
            original_text="Test incident for evidence",
        ),
    )

    evidence = create_evidence(
        db,
        EvidenceCreate(
            incident_id=incident.incident_id,
            evidence_type="application_log",
            source_type="UPLOAD",
            excerpt="HTTP 503",
            payload={"status_code": 503},
        ),
    )

    found = get_evidence(db, evidence.evidence_id)

    assert found is not None
    assert found.incident_id == incident.incident_id
    assert found.payload["status_code"] == 503


def test_list_evidence_for_incident(db):
    incident = create_incident(
        db,
        IncidentCreate(
            title="pytest repository test - evidence list",
            original_text="Test evidence listing",
        ),
    )

    evidence = create_evidence(
        db,
        EvidenceCreate(
            incident_id=incident.incident_id,
            evidence_type="application_log",
            source_type="UPLOAD",
            payload={"message": "Service unavailable"},
        ),
    )

    results = list_evidence_for_incident(db, incident.incident_id)

    assert any(item.evidence_id == evidence.evidence_id for item in results)
