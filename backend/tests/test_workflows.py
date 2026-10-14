from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_checkin_creates_structured_skin_state() -> None:
    response = client.post(
        "/api/users/demo-user-001/checkin",
        json={
            "feeling": "Tight",
            "appearance": "More dry than usual",
            "irritation": "Mild",
            "outdoor_exposure": "30-60 minutes",
            "sunscreen": "Yes",
            "routine": "Complete",
            "note": "Felt tight after commuting",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "DAILY_CHECKIN"
    assert body["dryness_indicator"] >= 55


def test_device_readings_are_explicitly_simulated() -> None:
    response = client.get("/api/devices/demo-device-001/readings")

    assert response.status_code == 200
    assert response.json()[0]["data_quality"] == "SIMULATED"
