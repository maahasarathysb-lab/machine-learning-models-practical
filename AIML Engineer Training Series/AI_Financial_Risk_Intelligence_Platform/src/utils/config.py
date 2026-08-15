from pathlib import Path

# ============================================================
# Project Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODEL_DIR = PROJECT_ROOT / "models"
NOTEBOOK_DIR = PROJECT_ROOT / "notebooks"
APP_DIR = PROJECT_ROOT / "app"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"

GERMAN_DATA_PATH = RAW_DATA_DIR / "german.data"
MODEL_PATH = MODEL_DIR / "credit_risk_pipeline.joblib"

# ============================================================
# Dataset Columns
# ============================================================

COLUMN_NAMES = [
    "status", "duration", "credit_history", "purpose", "credit_amount",
    "savings", "employment_duration", "installment_rate", "personal_status_sex",
    "other_debtors", "present_residence", "property", "age",
    "other_installment_plans", "housing", "existing_credits", "job",
    "people_liable", "telephone", "foreign_worker", "target"
]

# ============================================================
# Model Settings
# ============================================================

RANDOM_STATE = 42
TEST_SIZE = 0.20
RISK_THRESHOLD = 0.40