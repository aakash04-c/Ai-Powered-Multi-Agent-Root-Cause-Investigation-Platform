# testing first node recive incident

from app.workflow.nodes import receive_incident


def test_receive_incident_with_valid_data():
    # Arrange: Prepare input
    state = {
        "incident": {
            "incident_id": "INC-001",
            "title": "Payment service is down",
            "description": "Payments are failing",
            "affected_service": "payment-service",
            "occurred_at": "2026-10-24T09:30:00+05:30",
            "status": "pending",
            "severity": "high"
        }
    }

    # Act: Call the function
    result = receive_incident(state)

    # Assert: Check the output
    assert result["incident_id"] == "INC-001"
    assert result["status"] == "received"
    assert result["evidences"] == []
    assert result["errors"] == []

def test_receive_incident_with_missing_id():
    # Arrange: Prepare input
    state = {
        "incident": {
            "title": "Payment service is down",
            "description": "Payments are failing",
            "affected_service": "payment-service",
            "occurred_at": "2026-10-24T09:30:00+05:30",
            "status": "pending",
            "severity": "high"
        }
    }

    # Act: Call the function
    result = receive_incident(state)

    # Assert: Check the output
    
    assert result["status"] == "failed"
    assert result["errors"] == ["Incident ID is missing"]


def test_receive_incident_with_missing_data():
    # Arrange: Prepare input
    state = {
        # "incident": {
        #     "title": "Payment service is down",
        #     "description": "Payments are failing",
        #     "affected_service": "payment-service",
        #     "occurred_at": "2026-10-24T09:30:00+05:30",
        #     "status": "pending",
        #     "severity": "high"
        # }
    }

    # Act: Call the function
    result = receive_incident(state)

    # Assert: Check the output
    
    assert result["status"] == "failed"
    assert result["errors"] == ["Incident data is missing or invalid !"]


# tetsing 2nd node validate incident
from app.workflow.nodes import receive_incident,validate_incident

# tetsing with complete data
def test_validate_incident_with_valid_data():
    state = {
        "incident": {
            "incident_id": "INC-001",
            "title": "Payment service down",
            "description": "Users cannot make payments",
            "affected_service": "Payment Service",
            "occurred_at": "2026-10-24T10:00:00+05:30",
            "status": "pending",
            "severity": "high"
        },
        "evidences": [],
        "status": "received",
        "errors": []
    }

    result = validate_incident(state)
    print(result)

    assert result["status"] == "received"
    assert result["errors"] == []
    assert result["incident_id"] == "INC-001"

# testing with invalid data
def test_validate_incident_with_invalid_data():
    state = {
        "incident": {
            "incident_id": "INC-001",
            "title": "",
            "description": "Users cannot make payments",
            "affected_service": "Payment Service",
            "occurred_at": "2026-10-24T10:00:00+05:30",
            "status": "pending",
            "severity": "high"
        },
        "evidences": [],
        "status": "received",
        "errors": []
    }

    result = validate_incident(state)

    assert result["status"] == "failed"
    assert "title is required" in result["errors"]



# testing node 3 prepare incident

from app.workflow.nodes import prepare_investigation

# validate incident
def test_prepare_investigation_with_valid_data():
    state={
        
    }