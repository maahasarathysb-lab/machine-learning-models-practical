import pandas as pd

from src.utils.config import GERMAN_DATA_PATH, COLUMN_NAMES


def load_data():
    """Load the German Credit dataset."""

    df = pd.read_csv(
        GERMAN_DATA_PATH,
        sep=r"\s+",
        header=None,
        names=COLUMN_NAMES
    )

    # Convert target:
    # 1 -> Good Credit (0)
    # 2 -> Bad Credit (1)
    df["target"] = df["target"].map({1: 0, 2: 1})

    return df


if __name__ == "__main__":
    df = load_data()
    print(df.head())
    print(df.shape)