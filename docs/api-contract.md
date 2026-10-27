# REST API Contract (Sprint 1)

## Base URL
`/api`

---

## Core Endpoints Overview

| Method | Endpoint | Purpose | Request Body | Response |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/incidents` | Create a new incident record | `IncidentCreate` | `201 Created` (`IncidentResponse`) |
| `GET` | `/api/incidents` | List all incidents | None (optional query params) | `200 OK` (`list[IncidentResponse]`) |
| `GET` | `/api/incidents/{id}` | Retrieve incident details | None | `200 OK` (`IncidentResponse`) |
| `POST` | `/api/incidents/{id}/evidence` | Ingest evidence associated with an incident | `EvidenceCreate` (or payload without id) | `201 Created` (`EvidenceResponse`) |
| `GET` | `/api/incidents/{id}/evidence` | List all evidence items for an incident | None | `200 OK` (`list[EvidenceResponse]`) |
| `POST` | `/api/incidents/{id}/investigate` | Trigger the LangGraph state machine workflow | None | `200 OK` (`InvestigationState`) |
| `GET` | `/api/incidents/{id}/state` | Inspect current investigation workflow state | None | `200 OK` (`InvestigationState`) |

---

## Benchmark & Scenario Ingestion Strategy

Rather than maintaining a separate or proprietary "benchmark loader" endpoint in backend application code, **all telemetry—including benchmark scenarios (`scenario_01`, `scenario_02`, `scenario_03`)—is ingested exclusively through the standard production REST API endpoints**:

1. **Incident Creation**: Benchmark incidents are submitted via `POST /api/incidents`.
2. **Evidence Ingestion**: Benchmark telemetry items are submitted via `POST /api/incidents/{id}/evidence` with `"source_type": "BENCHMARK"`.
3. **Automated Verification**: Pytest suites load test datasets from `data/scenarios/` and verify the complete ingestion and state preparation pipeline through the standard HTTP interface.

This ensures:
- Full end-to-end testing of Pydantic schemas, database constraints, and API routing.
- Zero code duplication between test loaders and production ingestion paths.
- Total decoupling of the backend service from local filesystem dependencies.

---

## Detailed Endpoint Specifications

### 1. Create Incident
* **URL**: `POST /api/incidents`
* **Status**: `201 Created`
* **Request Payload**:
  ```json
  {
    "title": "Database connection pool exhausted",
    "original_text": "The order service started returning HTTP 500 errors because PostgreSQL connections were saturated.",
    "affected_service": "order-service",
    "severity": "SEV1",
    "started_at": "2026-10-24T09:30:00+05:30"
  }
  ```
* **Response Payload**:
  ```json
  {
    "incident_id": "c1f8a847-a8d2-4b2a-89bc-9937bc38d9b1",
    "title": "Database connection pool exhausted",
    "original_text": "The order service started returning HTTP 500 errors because PostgreSQL connections were saturated.",
    "affected_service": "order-service",
    "severity": "SEV1",
    "status": "OPEN",
    "started_at": "2026-10-24T09:30:00+05:30",
    "ended_at": null,
    "created_at": "2026-10-24T09:35:12+05:30",
    "updated_at": "2026-10-24T09:35:12+05:30"
  }
  ```

---

### 2. List Incidents
* **URL**: `GET /api/incidents?limit=50&offset=0`
* **Status**: `200 OK`
* **Response Payload**: `list[IncidentResponse]`

---

### 3. Get Incident
* **URL**: `GET /api/incidents/{incident_id}`
* **Status**: `200 OK` (or `404 Not Found`)
* **Response Payload**: `IncidentResponse`

---

### 4. Ingest Evidence Item
* **URL**: `POST /api/incidents/{incident_id}/evidence`
* **Status**: `201 Created`
* **Request Payload**:
  ```json
  {
    "evidence_type": "ticket",
    "source_type": "BENCHMARK",
    "source_name": "jira",
    "source_record_id": "JIRA-501",
    "event_time": "2026-10-24T09:32:00+05:30",
    "excerpt": "Multiple users reporting timeouts when placing orders during checkout.",
    "original_ref": "https://jira.company.com/browse/JIRA-501",
    "reliability_score": 0.9500,
    "payload": {
      "reporter": "alice@company.com",
      "priority": "Highest"
    }
  }
  ```
* **Response Payload**: `EvidenceResponse`

---

### 5. List Evidence for Incident
* **URL**: `GET /api/incidents/{incident_id}/evidence`
* **Status**: `200 OK`
* **Response Payload**: `list[EvidenceResponse]`

---

### 6. Run LangGraph Preparation Workflow
* **URL**: `POST /api/incidents/{incident_id}/investigate`
* **Status**: `200 OK`
* **Response Payload**:
  ```json
  {
    "incident_id": "c1f8a847-a8d2-4b2a-89bc-9937bc38d9b1",
    "status": "READY",
    "errors": [],
    "completed_at": "2026-10-24T09:36:00.123456+00:00"
  }
  ```

---

### 7. Get Investigation State
* **URL**: `GET /api/incidents/{incident_id}/state`
* **Status**: `200 OK`
* **Response Payload**: `InvestigationState`
