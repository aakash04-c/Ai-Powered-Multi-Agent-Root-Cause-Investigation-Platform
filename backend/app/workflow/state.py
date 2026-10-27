from typing import TypedDict


class InvestigationState(TypedDict, total=False):
    incident_id: str
    incident: dict
    evidences: list[dict]
    status: str
    errors: list[str]
    completed_at: str
