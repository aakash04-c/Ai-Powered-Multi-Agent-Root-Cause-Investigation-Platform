from typing import TypedDict


class InvestigationState(TypedDict, total=False):
    # Identifier used to track the incident through the workflow.
    incident_id: str
    # Original incident payload received by the workflow.
    incident: dict
    # Evidence associated with the incident; nodes preserve this list.
    evidences: list[dict]
    # Current workflow stage, such as validated, prepared, failed, or READY.
    status: str
    # Validation or processing errors; an empty list means no errors occurred.
    errors: list[str]
    # UTC timestamp added when the investigation reaches the READY stage.
    completed_at: str