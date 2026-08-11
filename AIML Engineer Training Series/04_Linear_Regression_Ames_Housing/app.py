from fastapi import FastAPI
import joblib
import pandas as pd
from pathlib import Path

app = FastAPI(title="Ames Housing Price Prediction API")

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "ridge_model.pkl"
DATA_PATH = BASE_DIR / "data" / "train.csv"

model = joblib.load(MODEL_PATH)

@app.get("/")
def home():
    return {
        "message": "Ames Housing Price Prediction API is running",
        "status": "success"
    }

@app.post("/predict")
def predict():
    sample = pd.read_csv(DATA_PATH).drop(columns=["SalePrice"]).iloc[[0]]
    prediction = model.predict(sample)[0]
    return {
        "predicted_sale_price": round(float(prediction), 2)
    }