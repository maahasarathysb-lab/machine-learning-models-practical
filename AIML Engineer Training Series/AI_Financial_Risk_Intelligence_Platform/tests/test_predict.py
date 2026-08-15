from src.models.predict import CreditRiskPredictor


def test_prediction_output_structure():
    predictor = CreditRiskPredictor()

    sample = {
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

    result = predictor.predict(sample)

    assert "default_probability" in result
    assert "prediction" in result
    assert "risk_level" in result

    assert 0.0 <= result["default_probability"] <= 1.0
    assert result["prediction"] in ["Good Credit", "Bad Credit"]
    assert result["risk_level"] in ["Low", "Medium", "High"]