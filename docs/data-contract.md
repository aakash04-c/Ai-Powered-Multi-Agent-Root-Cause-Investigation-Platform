# Data Contracts — Sprint 1
## AI-Powered Root Cause Investigation Platform

## 1. Purpose

This document defines the data structures and validation rules used in Sprint 1 of the AI-Powered Root Cause Investigation Platform.

The purpose of these contracts is to ensure that incident data and supporting evidence follow a consistent format when they are received, validated, stored, and passed into the LangGraph workflow.

For Sprint 1, the platform focuses on:
- Defining a standard incident structure.
- Defining a standard evidence structure.
- Validating incoming data.
- Associating evidence with the correct incident.
- Preparing incident data for the LangGraph investigation workflow.
- Supporting workflow state persistence and retrieval through a configured checkpointer.

The platform initially uses software engineering incidents as demonstration scenarios. The data contracts should remain reusable for other types of investigations in the future.

## 2. Scope

### In Scope
- Incident data contract.
- Evidence data contract.
- Basic API request and response expectations.
- Data validation rules.
- LangGraph investigation state schema.
- Incident and evidence association.
- Basic workflow status tracking.

### Out of Scope
- AI-generated root-cause hypotheses.
- Causal DAG construction.
- Evidence relevance and reliability scoring.
- Contradiction analysis.
- Automated fix generation.
- Final root-cause report schema.

These features can be introduced in later sprints when their corresponding workflows are implemented.

## 3. Incident Data Contract

An incident represents the problem that the platform is expected to investigate.

### 3.1 Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `incident_id` | String | Yes | Unique identifier for the incident. |
| `title` | String | Yes | Short description of the problem. |
| `description` | String | Yes | Detailed description of the observed problem. |
| `affected_service` | String | Yes | Service or component affected by the incident. |
| `occurred_at` | ISO 8601 datetime | Yes | Time when the incident began or was first observed. |
| `status` | String | Yes | Current incident lifecycle status. |
| `severity` | String | No | Optional indication of incident impact. |

### 3.2 Example

```json
{
  "incident_id": "INC-001",
  "title": "Database connection pool exhausted",
  "description": "The order service started returning API errors because database connections were unavailable. Request latency increased, and some requests timed out.",
  "affected_service": "order-service",
  "occurred_at": "2026-10-23T14:30:00Z",
  "status": "pending",
  "severity": "high"
}
```

This is a synthetic demonstration incident, not a real production incident.

### 3.3 Validation Rules

- `incident_id` must be non-empty and unique.
- `title`, `description`, and `affected_service` must not be empty.
- `occurred_at` must be a valid ISO 8601 datetime with timezone information.
- `status` must use an explicitly defined set of allowed values.
- If provided, `severity` must be one of the following values:
  - `low`
  - `medium`
  - `high`
  - `critical`

### 3.4 Severity Definitions

| Severity | Meaning | Example |
|---|---|---|
| `low` | Minimal impact on the system or users. | A minor warning with no noticeable user impact. |
| `medium` | Noticeable but limited impact. | An API is slow, but most requests succeed. |
| `high` | Significant impact on users or an important service. | Many users experience failed order requests. |
| `critical` | Severe impact, such as a major service outage. | The entire ordering system is unavailable. |

These definitions are initial project conventions and can be refined as the platform develops.

### 3.5 Incident Lifecycle Status

For the initial implementation, the incident status may use:
- `pending`
- `investigating`
- `resolved`
- `closed`

These values describe the incident lifecycle. They should not be confused with severity or LangGraph workflow execution status.

## 4. Evidence Data Contract

Evidence represents a record of information that may help explain an incident.

During Sprint 1, evidence can originate from:
- Jira incident tickets.
- Deployment logs.
- Slack incident threads.
- Metrics.

Evidence must be stored separately from the incident so that multiple evidence records can be associated with one incident.

### 4.1 Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `evidence_id` | String | Yes | Unique identifier assigned to the evidence record by our platform. |
| `incident_id` | String | Yes | Identifier of the incident associated with the evidence. |
| `source` | String | Yes | Origin of the evidence. |
| `timestamp` | ISO 8601 datetime | Yes | Time associated with the original event, message, or record. |
| `content` | String | Yes | Text or relevant information extracted from the source. |
| `source_reference` | String or null | No | Identifier or locator for the original source record. |

### 4.2 Example

```json
[
  {
    "evidence_id": "EV-001",
    "incident_id": "INC-001",
    "source": "jira",
    "timestamp": "2026-10-23T14:35:00Z",
    "content": "Multiple users report order API timeouts. Database connection acquisition is failing.",
    "source_reference": "JIRA-501"
  },
  {
    "evidence_id": "EV-002",
    "incident_id": "INC-001",
    "source": "deployment_log",
    "timestamp": "2026-10-23T14:20:00Z",
    "content": "Database connection pool maximum was changed from 100 to 20 during deployment.",
    "source_reference": "DEPLOY-204"
  },
  {
    "evidence_id": "EV-003",
    "incident_id": "INC-001",
    "source": "slack",
    "timestamp": "2026-10-23T14:38:00Z",
    "content": "The team reports that connection usage reached the configured limit shortly after deployment.",
    "source_reference": "SLACK-MSG-88"
  }
]
```

All records above are synthetic examples created for demonstration purposes.

### 4.3 Allowed Sources

The `source` field must use one of the following values:

| Value | Meaning |
|---|---|
| `jira` | Evidence originating from Jira. |
| `deployment_log` | Evidence originating from deployment logs. |
| `slack` | Evidence originating from Slack incident threads. |

Additional sources may be introduced in future iterations if required.

### 4.4 Validation Rules

- `evidence_id` must be non-empty and unique.
- `incident_id` must reference an existing incident.
- `source` must match one of the allowed source values.
- `timestamp` must be a valid ISO 8601 datetime with timezone information.
- `content` must not be empty.
- `source_reference` may be null when the original system does not provide a usable reference.
- Evidence must remain associated with its corresponding incident during storage and retrieval.

The platform must not treat evidence as confirmed proof of a root cause merely because it has been ingested.

## 5. Meaning of `source_reference`

The `source_reference` field identifies the original record from which the evidence was obtained.

Examples:
- Jira issue key, such as `JIRA-501`.
- Deployment identifier or log record ID, such as `DEPLOY-204`.
- Slack message ID, thread ID, or permalink.

The distinction between identifiers is important:

- `incident_id` identifies an incident within our platform.
- `evidence_id` identifies an evidence record within our platform.
- `source_reference` identifies or locates the original record in an external source system.

For Sprint 1, storing source references is sufficient. Automatic navigation to or retrieval from external systems is not required unless included in the agreed ingestion scope.

## 6. Evidence Collection Format

An incident may contain multiple evidence records. The evidence collection format groups those records for loading and processing.

For the initial scenario-based implementation, evidence may be represented as a JSON array in an `evidences.json` file.

Example directory structure:

```text
data/
└── scenarios/
    └── database_connection_leak/
        ├── incident.json
        └── evidences.json
```

The scenario directory groups the sample files for testing and demonstration. In persistent storage, incidents and evidence records should be stored separately and associated through `incident_id`.

## 7. API Request and Response Expectations

The API layer is responsible for validating external input and returning predictable responses.

### 7.1 Create Incident Request

The incident creation endpoint should accept a payload matching the incident data contract.

Example:

```http
POST /api/v1/incidents
Content-Type: application/json
```

Request body:

```json
{
  "incident_id": "INC-001",
  "title": "Database connection pool exhausted",
  "description": "The order API is experiencing database connection timeouts.",
  "affected_service": "order-service",
  "occurred_at": "2026-10-23T14:30:00Z",
  "status": "pending",
  "severity": "high"
}
```

The final endpoint path and whether `incident_id` is client-generated or server-generated must be consistent with the implemented API design.

### 7.2 Response Expectations

A successful creation response should provide:
- The incident identifier.
- The accepted incident details or a reference to the created incident.
- A clear success status.

Invalid input should produce an appropriate HTTP error response with a useful validation message.

The API should not expose stack traces, credentials, or sensitive internal information in error responses.

## 8. LangGraph Investigation State

The LangGraph state defines the information carried between nodes during an investigation workflow.

It is a workflow schema, not a replacement for the incident or evidence data contracts.

### 8.1 Initial State Schema

```python
from typing import TypedDict


class InvestigationState(TypedDict):
    incident_id: str
    incident: dict
    evidences: list[dict]
    status: str
    errors: list[str]
```

### 8.2 Field Descriptions

| Field | Type | Purpose |
|---|---|---|
| `incident_id` | String | Identifies the incident being processed. |
| `incident` | Dictionary | Holds the validated incident details. |
| `evidences` | List of dictionaries | Holds the evidence records loaded for the incident. |
| `status` | String | Tracks the current workflow stage. |
| `errors` | List of strings | Stores validation or processing errors. |

This schema is intentionally minimal for Sprint 1. Dedicated nested types may replace generic dictionaries as the implementation matures.

### 8.3 Example Workflow Status Values

The initial workflow may use these values:

- `received`: The incident has entered the workflow.
- `evidence_loaded`: Evidence has been retrieved and added to the state.
- `ready`: Required preparation and validation have completed.
- `failed`: A blocking error prevented the workflow from completing preparation.

These values describe workflow execution. They do not replace the incident lifecycle status.

### 8.4 State Updates

LangGraph nodes may return partial state updates instead of reconstructing the entire state.

For example:

```python
return {
    "evidences": loaded_evidences,
    "status": "evidence_loaded"
}
```

LangGraph applies the node's updates to the existing state according to the graph's state update semantics and any configured reducers.

## 9. Persistence and Thread Identification

Sprint 1 must demonstrate that investigation state can be persisted and retrieved.

A configured LangGraph checkpointer saves graph state at checkpoints. A persistent checkpointer implementation must be selected and configured to retain that state in the intended storage system.

The graph should be invoked with a stable `thread_id` through its runtime configuration.

Example:

```python
config = {
    "configurable": {
        "thread_id": "investigation-INC-001"
    }
}
```

The incident ID and thread ID serve different purposes:

- `incident_id` identifies the problem being investigated.
- `thread_id` identifies the LangGraph execution history used for checkpointing and resumption.

The thread ID must remain consistent when retrieving or resuming the same investigation. A checkpointer and suitable storage configuration are required; defining a `TypedDict` alone does not provide persistence.

## 10. Data Validation and Consistency

Validation should occur before invalid data is stored or passed into the workflow.

The initial implementation should check:

1. Required fields are present.
2. Field values have the expected types.
3. Identifiers are unique within their intended scope.
4. Datetimes are valid and timezone-aware.
5. Evidence source values belong to the supported set.
6. Evidence references an existing incident.
7. Severity, when provided, is one of `low`, `medium`, `high`, or `critical`.
8. Incident status uses an allowed value.
9. Empty or malformed content is rejected where required.
10. Invalid data produces clear, structured error responses.

Pydantic models should be used for API-boundary validation. Database constraints should enforce appropriate uniqueness and relationship rules where supported.

Validation must not assume that syntactically valid evidence is factually correct.

## 11. Data Storage Principles

The initial data design follows these principles:

- Incident records and evidence records remain logically separate.
- Each evidence record is associated with an incident using `incident_id`.
- External source identifiers are retained when available.
- Incident and evidence timestamps use consistent timezone-aware representations.
- Only the data needed for the current workflow should be loaded into LangGraph state.
- Checkpoint persistence is configured separately from the incident and evidence storage design.

The final database tables, collections, and checkpoint storage implementation should be documented in the architecture and database design documents.

## 12. Sprint 1 Acceptance Criteria

The data-contract implementation is considered complete when:

- [ ] Incident and evidence schemas are defined.
- [ ] Required fields and allowed values are documented.
- [ ] Synthetic incident and evidence fixtures are available.
- [ ] Invalid payloads fail validation with useful errors.
- [ ] Evidence records are associated with the correct incident.
- [ ] Incident and evidence data can be loaded through the intended ingestion path.
- [ ] Validated data can initialize and update the LangGraph state.
- [ ] Workflow status and processing errors can be represented in state.
- [ ] A configured checkpointer can persist and retrieve state using the same `thread_id`.
- [ ] Tests cover valid input, invalid input, evidence association, and checkpoint retrieval.

## 13. Future Extensions

The following contracts and fields may be added in later sprints when the corresponding capabilities are implemented:

- Hypothesis contract for proposed root causes and supporting evidence.
- Evidence evaluation contract for relevance, reliability, and contradictory information.
- Causal graph contract for causal nodes and directed relationships.
- Investigation result contract for final findings and recommendations.
- Additional source metadata for richer external traceability.

These extensions are intentionally excluded from the Sprint 1 implementation scope.

## 14. Summary

Sprint 1 establishes a consistent data foundation for the AI Root Cause Investigation Platform.

The incident contract defines the problem, the evidence contract defines the supporting records, the API layer validates incoming data, and the LangGraph state schema defines the data carried through the workflow.

Together, these components allow the team to demonstrate incident ingestion, evidence association, workflow preparation, and checkpoint persistence before introducing AI-driven causal investigation in subsequent sprints.