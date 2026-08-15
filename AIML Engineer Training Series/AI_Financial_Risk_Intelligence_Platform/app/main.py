from fastapi import FastAPI
from pydantic import BaseModel

from src.models.predict import CreditRiskPredictor

# ============================================================
# Load Predictor
# ============================================================

predictor = CreditRiskPredictor()

# ============================================================
# FastAPI App
# ============================================================

app = FastAPI(
    title="AI Financial Risk Intelligence Platform",
    version="1.0.0",
    description="Credit Risk Prediction API using Logistic Regression"
)

# ============================================================
# Request Schema
# ============================================================

class CreditApplication(BaseModel):
    status: str
    duration: int
    credit_history: str
    purpose: str
    credit_amount: int
    savings: str
    employment_duration: str
    installment_rate: int
    personal_status_sex: str
    other_debtors: str
    present_residence: int
    property: str
    age: int
    other_installment_plans: str
    housing: str
    existing_credits: int
    job: str
    people_liable: int
    telephone: str
    foreign_worker: str

# ============================================================
# Health Check
# ============================================================

@app.get("/")
def home():
    return {
        "message": "AI Financial Risk Intelligence Platform API",
        "status": "running"
    }

# ============================================================
# Prediction Endpoint
# ============================================================

@app.post("/predict")
def predict(application: CreditApplication):
    return predictor.predict(application.model_dump())