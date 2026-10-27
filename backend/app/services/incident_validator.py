from datetime import datetime
from typing import Any, Dict, List, Optional


ALLOWED_STATUSES = {
    "OPEN",
    "INVESTIGATING",
    "RESOLVED",
    "CLOSED",
    # Legacy/draft status alias:
    "PENDING",
}

ALLOWED_SEVERITIES = {
    "SEV1",
    "SEV2",
    "SEV3",
    "SEV4",
    "UNKNOWN",
    # Legacy/draft severity aliases:
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
}


def validate_incident_data(incident: Dict[str, Any]) -> List[str]:
    """
    Validates an incident dictionary against the platform data contracts
    and database model constraints.
    """
    errors: List[str] = []

    # 1. Check incident dictionary type
    if not isinstance(incident, dict):
        return ["Incident must be dictionary"]

    # 2. Validate incident_id
    incident_id = incident.get("incident_id")
    if incident_id is None or not str(incident_id).strip():
        errors.append("incident_id is required")

    # 3. Validate title
    title = incident.get("title")
    if not isinstance(title, str) or not title.strip():
        errors.append("title is required")
    elif len(title) > 200:
        errors.append("title must not exceed 200 characters")

    # 4. Validate problem description (accepts 'original_text' or legacy 'description')
    problem_text = incident.get("original_text") or incident.get("description")
    if problem_text is not None and not isinstance(problem_text, str):
        errors.append("original_text/description must be a string")

    # 5. Validate affected_service
    affected_service = incident.get("affected_service")
    if affected_service is not None and not isinstance(affected_service, str):
        errors.append("affected_service must be a string")

    # 6. Validate start/occurred timestamp
    start_time_str = incident.get("started_at") or incident.get("occurred_at")
    parsed_start_time: Optional[datetime] = None

    if start_time_str is not None:
        if not isinstance(start_time_str, str) or not start_time_str.strip():
            errors.append("occured_at is required")
        else:
            try:
                parsed_start_time = datetime.fromisoformat(start_time_str)
                if (
                    parsed_start_time.tzinfo is None
                    or parsed_start_time.utcoffset() is None
                ):
                    errors.append("occured_at must include a timezone")
            except (ValueError, TypeError):
                errors.append("occured_at must be a valid ISO 8601 datetime")

    # 7. Validate ended timestamp (if provided)
    end_time_str = incident.get("ended_at")
    if end_time_str is not None:
        if not isinstance(end_time_str, str) or not end_time_str.strip():
            errors.append("ended_at must be a valid ISO 8601 datetime string")
        else:
            try:
                parsed_end_time = datetime.fromisoformat(end_time_str)
                if (
                    parsed_end_time.tzinfo is None
                    or parsed_end_time.utcoffset() is None
                ):
                    errors.append("ended_at must include a timezone")
                elif parsed_start_time and parsed_end_time < parsed_start_time:
                    errors.append("ended_at cannot be earlier than started_at")
            except (ValueError, TypeError):
                errors.append("ended_at must be a valid ISO 8601 datetime")

    # 8. Validate incident status
    status = incident.get("status")
    if status is not None:
        if not isinstance(status, str) or status.strip().upper() not in ALLOWED_STATUSES:
            errors.append("status is invalid")

    # 9. Validate severity (case-insensitive key and value)
    severity = incident.get("severity")
    if severity is None:
        severity = incident.get("Severity")

    if severity is not None:
        if not isinstance(severity, str) or severity.strip().upper() not in ALLOWED_SEVERITIES:
            errors.append("Severity is invalid")

    return errors