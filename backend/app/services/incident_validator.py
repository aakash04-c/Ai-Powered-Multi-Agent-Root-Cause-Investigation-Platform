from datetime import datetime

def validate_incident_data(incident: dict)-> list[str]:
    errors=[]

    # check incident data
    if not isinstance(incident,dict):
        return ["Incident must be dictionary"]

    # validate incident_id
    incident_id=incident.get("incident_id")

    if not isinstance(incident_id, str) or not incident_id.strip():
        errors.append("incident_id is required")

    # validate title
    title=incident.get("title")

    if not isinstance(title , str) or not title.strip():
        errors.append("title is required")

    # validate affected services
    affected_service = incident.get("affected_service")

    if not isinstance(affected_service, str) or not affected_service.strip(): 
        errors.append("affected_service is required")

    # validate occured at
    occured_at=incident.get("occurred_at")

    if not isinstance(occured_at , str) or not occured_at.strip():
        errors.append("occured_at is required")
    else:
        try:
            parsed_datetime=datetime.fromisoformat(occured_at)

            if(
                parsed_datetime.tzinfo is None
                or parsed_datetime.utcoffset() is None
            ):
                errors.append("occured_at must include a timezone")
        except ValueError:
            errors.append(
                "occured_at must be a valid ISO 8601 datetime"
            )


    # validate incident status
    allowed_statuses={
        "pending",
        "investigating",
        "resolved",
        "closed",
    }

    status=incident.get("status")

    if not isinstance(status,str) or status not in allowed_statuses:
        errors.append("status is invalid")

    # validate severity

    allowed_severity={
        "low",
        "medium",
        "high",
        "critical",
    }

    severity=incident.get("Severity")

    if severity is not None:
        if(
            not isinstance(severity,str)
            or severity not in allowed_severity
        ):
            errors.append("Severity is invalid")

    return errors