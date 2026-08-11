import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error

from preprocess import create_preprocessor


def train_model(data_path, target_column="SalePrice"):
    # Load dataset
    df = pd.read_csv(data_path)

    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Preprocessor
    preprocessor = create_preprocessor(df, target_column)

    # Ridge Regression Pipeline
    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", Ridge(alpha=1.0))
    ])

    # Train
    model.fit(X_train, y_train)

    # Predict
    predictions = model.predict(X_test)

    # Metrics
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    rmse = root_mean_squared_error(y_test, predictions)

    print("Model Performance")
    print(f"R² Score : {r2:.4f}")
    print(f"MAE      : {mae:.2f}")
    print(f"RMSE     : {rmse:.2f}")

    # Save model
    os.makedirs("../models", exist_ok=True)
    joblib.dump(model, "../models/ridge_model.pkl")

    print("Model saved to models/ridge_model.pkl")


if __name__ == "__main__":
    train_model("../data/train.csv")