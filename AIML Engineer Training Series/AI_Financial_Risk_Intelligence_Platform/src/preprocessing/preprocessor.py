from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def build_preprocessor(X_train):
    """Build the preprocessing pipeline for numerical and categorical features."""

    categorical_cols = X_train.select_dtypes(include="object").columns.tolist()
    numerical_cols = X_train.select_dtypes(exclude="object").columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
        ]
    )

    return preprocessor, numerical_cols, categorical_cols