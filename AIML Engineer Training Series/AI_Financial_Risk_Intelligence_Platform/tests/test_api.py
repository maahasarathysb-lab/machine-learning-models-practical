from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


def test_predict_endpoint():
    payload = {
        "status": "A11",
        "duration": 24,
        "credit_history": "A30",
        "purpose": "A40",
        "credit_amount": 4500,
        "savings": "A61",
        "employment_duration": "A72",
        "installment_rate": 4,
        "personal_status_sex": "A93",
        "other_debtors": "A101",
        "present_residence": 2,
        "property": "A121",
        "age": 30,
        "other_installment_plans": "A143",
        "housing": "A152",
        "existing_credits": 1,
        "job": "A173",
        "people_liable": 1,
        "telephone": "A191",
        "foreign_worker": "A201"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "default_probability" in data
    assert "prediction" in data
    assert "risk_level" in data