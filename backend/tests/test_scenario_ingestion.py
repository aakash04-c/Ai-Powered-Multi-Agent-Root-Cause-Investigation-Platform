import json
from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.db.database import SessionLocal
from app.db.models import EvidenceItem, Incident
from app.main import app

client = TestClient(app)

SCENARIOS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "scenarios"


@pytest.fixture(autouse=True)
def cleanup_benchmark_test_data():
    """Ensure benchmark test records are cleaned up after each test."""
    yield
    session = SessionLocal()
    try:
        benchmark_incidents = (
            session.query(Incident)
            .filter(
                Incident.title.in_(
                    [
                        "Database connection pool exhausted",
                        "Payment gateway memory leak and container OOMKilled",
                        "Auth service latency spike due to third-party identity provider throttling",
                    ]
                )
            )
            .all()
        )
        incident_ids = [inc.incident_id for inc in benchmark_incidents]
        if incident_ids:
            session.query(EvidenceItem).filter(
                EvidenceItem.incident_id.in_(incident_ids)
            ).delete(synchronize_session=False)
            session.query(Incident).filter(
                Incident.incident_id.in_(incident_ids)
            ).delete(synchronize_session=False)
            session.commit()
    finally:
        session.close()


def test_scenario_01_api_ingestion_and_investigation():
    """Upload scenario_01 via standard REST API and trigger LangGraph preparation."""
    scenario_path = SCENARIOS_DIR / "scenario_01"

    # 1. Load synthetic incident file
    with open(scenario_path / "incident.json", encoding="utf-8") as f:
        incident_payload = json.load(f)

    # 2. Ingest incident via standard API
    res = client.post("/api/incidents", json=incident_payload)
    assert res.status_code == 201
    created_incident = res.json()
    incident_id = created_incident["incident_id"]
    assert UUID(incident_id)
    assert created_incident["severity"] == "SEV1"
    assert created_incident["status"] == "OPEN"

    # 3. Load and ingest all evidence items via standard API
    with open(scenario_path / "evidences.json", encoding="utf-8") as f:
        evidences = json.load(f)

    for item in evidences:
        ev_res = client.post(f"/api/incidents/{incident_id}/evidence", json=item)
        assert ev_res.status_code == 201
        evidence_data = ev_res.json()
        assert evidence_data["incident_id"] == incident_id
        assert evidence_data["source_type"] == "BENCHMARK"

    # 4. Verify evidence listing API
    list_res = client.get(f"/api/incidents/{incident_id}/evidence")
    assert list_res.status_code == 200
    assert len(list_res.json()) == len(evidences)

    # 5. Trigger workflow via standard API
    inv_res = client.post(f"/api/incidents/{incident_id}/investigate")
    assert inv_res.status_code == 200
    inv_data = inv_res.json()
    assert inv_data["status"] == "READY"
    assert inv_data["errors"] == []
    assert "completed_at" in inv_data


def test_scenario_02_api_ingestion():
    """Upload scenario_02 (OOMKill) via standard REST API."""
    scenario_path = SCENARIOS_DIR / "scenario_02"

    with open(scenario_path / "incident.json", encoding="utf-8") as f:
        incident_payload = json.load(f)

    res = client.post("/api/incidents", json=incident_payload)
    assert res.status_code == 201
    incident_id = res.json()["incident_id"]

    with open(scenario_path / "evidences.json", encoding="utf-8") as f:
        evidences = json.load(f)

    for item in evidences:
        ev_res = client.post(f"/api/incidents/{incident_id}/evidence", json=item)
        assert ev_res.status_code == 201

    inv_res = client.post(f"/api/incidents/{incident_id}/investigate")
    assert inv_res.status_code == 200
    assert inv_res.json()["status"] == "READY"


def test_scenario_03_api_ingestion():
    """Upload scenario_03 (IDP throttling) via standard REST API."""
    scenario_path = SCENARIOS_DIR / "scenario_03"

    with open(scenario_path / "incident.json", encoding="utf-8") as f:
        incident_payload = json.load(f)

    res = client.post("/api/incidents", json=incident_payload)
    assert res.status_code == 201
    incident_id = res.json()["incident_id"]

    with open(scenario_path / "evidences.json", encoding="utf-8") as f:
        evidences = json.load(f)

    for item in evidences:
        ev_res = client.post(f"/api/incidents/{incident_id}/evidence", json=item)
        assert ev_res.status_code == 201

    inv_res = client.post(f"/api/incidents/{incident_id}/investigate")
    assert inv_res.status_code == 200
    assert inv_res.json()["status"] == "READY"
