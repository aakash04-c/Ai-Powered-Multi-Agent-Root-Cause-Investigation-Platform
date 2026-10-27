from app.workflow.graph import build_investigation_graph


def test_graph_invocation_reaches_ready():
    graph = build_investigation_graph()
    initial_state = {
        "incident": {
            "incident_id": "INC-001",
            "title": "Payment service outage",
            "affected_service": "payments",
            "occurred_at": "2026-10-24T10:00:00+05:30",
            "status": "pending",
        }
    }

    result = graph.invoke(initial_state)

    assert result["status"] == "READY"
    assert result["incident_id"] == "INC-001"
    assert result["errors"] == []
    assert "completed_at" in result


def test_graph_invocation_stops_for_invalid_incident():
    graph = build_investigation_graph()
    initial_state = {
        "incident": {
            "incident_id": "INC-002",
            "title": "",
            "affected_service": "payments",
            "occurred_at": "2026-10-24T10:00:00+05:30",
            "status": "pending",
        }
    }

    result = graph.invoke(initial_state)

    assert result["status"] == "failed"
    assert "title is required" in result["errors"]
