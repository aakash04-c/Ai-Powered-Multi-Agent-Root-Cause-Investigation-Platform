# AI-Powered Root-Cause Investigation Platform

An evidence-driven platform designed to ingest multi-source incident telemetry, organize supporting evidence, and prepare structured states for causal root-cause analysis.

---

## Sprint 1: Foundation & Workflow Orchestration

Sprint 1 establishes the foundational data contracts, API boundaries, and state preparation workflow for incident investigations.

### Key Objectives
- **Standardized Data Contracts**: Pydantic models for incidents and evidence (supporting Jira, deployment logs, and Slack threads).
- **REST API Layer**: FastAPI service for incident intake, evidence ingestion, and state inspection.
- **LangGraph State Machine**: A deterministic 4-node preparation workflow (`Validate Incident` → `Load Evidence` → `Prepare Investigation State` → `Complete Preparation`).
- **State Persistence**: Checkpointing workflow state and retrieving execution snapshots using a stable `thread_id`.
- **Sample Benchmark Scenarios**: Synthetic software engineering incidents (e.g., database connection pool exhaustion) for local development and testing.

---

## Repository Structure

```text
root-cause-platform/
├── backend/                  # FastAPI backend service
│   ├── app/
│   │   ├── api/routes/       # REST API endpoint handlers
│   │   ├── core/             # Application configuration and settings
│   │   ├── db/               # Relational models and repositories
│   │   ├── schemas/          # Pydantic schemas (Incident, Evidence)
│   │   ├── services/         # Business logic and ingestion helpers
│   │   ├── workflow/         # LangGraph state graph and node definitions
│   │   └── main.py           # FastAPI application entrypoint
│   ├── tests/                # Automated pytest suite
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Sample environment configuration
├── data/
│   └── scenarios/            # Demonstration datasets (incident.json, evidences.json)
├── docs/                     # Architectural and interface specifications
│   ├── architecture.md       # Sprint 1 system architecture
│   ├── data-contract.md      # Incident, evidence, and state contract specifications
│   └── api-contract.md       # REST API endpoints and schemas
└── README.md
```

---

## Quickstart

### 1. Prerequisites
- Python 3.11+
- PostgreSQL (optional for local in-memory development, required for persistent storage)

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1    # On Windows PowerShell
# source venv/bin/activate     # On Linux / macOS

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
```

### 3. Run the Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

Once running, interactive API docs are available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 4. Run Tests

```bash
pytest
```

---

## Core API Endpoints (Sprint 1)

| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| `POST` | `/api/incidents` | Create an incident record |
| `POST` | `/api/incidents/{id}/evidence` | Ingest and associate evidence with an incident |
| `POST` | `/api/incidents/{id}/investigate` | Trigger/run the LangGraph preparation workflow |
| `GET` | `/api/incidents/{id}/state` | Retrieve persisted LangGraph checkpoint state |
| `GET` | `/api/incidents/{id}` | Retrieve incident details and evidence summary |

---

## Documentation Links

For detailed specifications, see:
- [System Architecture](docs/architecture.md)
- [Data Contracts & Schemas](docs/data-contract.md)
- [REST API Contract](docs/api-contract.md)
