import joblib
import pandas as pd

# Load trained model
model = joblib.load("../models/ridge_model.pkl")

# Load sample input
sample = pd.read_csv("../data/train.csv").drop(columns=["SalePrice"]).iloc[[0]]

# Predict
prediction = model.predict(sample)

print(f"Predicted Sale Price: ${prediction[0]:,.2f}")