import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "model")


def _load_model(filename: str):
    # Try loading from app/model first, then from current dir as fallback
    candidates = [
        os.path.join(MODELS_DIR, filename),
        os.path.join(BASE_DIR, filename),
    ]
    last_exc = None
    for path in candidates:
        try:
            if os.path.exists(path):
                return joblib.load(path)
        except Exception as e:
            last_exc = e
            continue
    raise FileNotFoundError(f"Model file not found: {filename} in {candidates}. Last error: {last_exc}")


delay_model = _load_model("delay_prediction_model.pkl")
cost_model = _load_model("cost_prediction_model.pkl")

FEATURE_COLUMNS = [
    "budget",
    "duration",
    "department",
    "project_type",
    "status",
    "region",
    "complexity",
    "completion_percent",
    "days_since_start",
    "benefit_cost_ratio",
    "cost_per_day",
    "project_Benefit",
    "project_Cost",
]

def predict_project_outcomes(data: dict):
    try:
        df = pd.DataFrame([data], columns=FEATURE_COLUMNS)
    except KeyError as e:
        raise ValueError(f"Missing input fields: {e}")

    delay_prob = delay_model.predict_proba(df)[0][1]
    delay_risk = "high" if delay_prob > 0.7 else "medium" if delay_prob > 0.4 else "low"

    cost_overrun = cost_model.predict(df)[0]

    return {
        "delay_probability": round(float(delay_prob), 2),
        "risk_level": delay_risk,
        "cost_overrun_estimate": round(float(cost_overrun), 2),
    }


