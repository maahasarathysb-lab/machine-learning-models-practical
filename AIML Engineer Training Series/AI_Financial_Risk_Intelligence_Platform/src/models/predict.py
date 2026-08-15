import joblib
import pandas as pd

from src.utils.config import MODEL_PATH, RISK_THRESHOLD


class CreditRiskPredictor:
    def __init__(self):
        self.pipeline = joblib.load(MODEL_PATH)

    def predict(self, application: dict):
        """Predict credit risk for a single applicant."""

        input_df = pd.DataFrame([application])

        probability = self.pipeline.predict_proba(input_df)[0, 1]

        prediction = int(probability >= RISK_THRESHOLD)

        risk_level = (
            "High" if probability >= 0.70
            else "Medium" if probability >= RISK_THRESHOLD
            else "Low"
        )

        return {
            "default_probability": round(float(probability), 4),
            "prediction": "Bad Credit" if prediction == 1 else "Good Credit",
            "risk_level": risk_level
        }


if __name__ == "__main__":
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

    print(predictor.predict(sample))