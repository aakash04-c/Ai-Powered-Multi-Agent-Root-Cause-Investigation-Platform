# REST API Contract (Sprint 1)

## Base URL
`/api`

## Core Endpoints Overview

| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| `POST` | `/api/incidents` | Create an incident |
| `POST` | `/api/incidents/{id}/evidence` | Save its evidence |
| `POST` | `/api/incidents/{id}/investigate` | Execute the LangGraph workflow |
| `GET` | `/api/incidents/{id}/state` | Retrieve persisted LangGraph state |
| `GET` | `/api/incidents/{id}` | Retrieve incident details |

---

## Additional Helper Endpoints (Benchmarks & Listing)

### List Incidents
- **`GET /api/incidents`**
  - **Purpose**: List all tracked incidents and their statuses.
  - **Response**: `200 OK` `list[IncidentResponse]`

### Load Synthetic Benchmarks
- **`POST /api/incidents/benchmark/load`**
  - **Purpose**: Seeds the synthetic multi-modal incident packages (`scenario_01`, `scenario_02`, `scenario_03`) into PostgreSQL.
  - **Response**: `200 OK` with summary of loaded benchmark scenarios.

