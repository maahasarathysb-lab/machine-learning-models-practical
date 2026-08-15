from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
import joblib

from src.preprocessing.data_loader import load_data
from src.preprocessing.preprocessor import build_preprocessor
from src.utils.config import MODEL_PATH, RANDOM_STATE, TEST_SIZE


def train_model():
    df = load_data()

    X = df.drop(columns="target")
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )

    preprocessor, _, _ = build_preprocessor(X_train)

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE))
        ]
    )

    pipeline.fit(X_train, y_train)

    joblib.dump(pipeline, MODEL_PATH)

    print(f"Model trained and saved to: {MODEL_PATH}")

    return pipeline


if __name__ == "__main__":
    train_model()