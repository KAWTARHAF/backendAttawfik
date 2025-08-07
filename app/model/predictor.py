import joblib
import pandas as pd


import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

delay_model = joblib.load(os.path.join(BASE_DIR, "delay_prediction_model.pkl"))
cost_model = joblib.load(os.path.join(BASE_DIR, "cost_prediction_model.pkl"))


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
    "project_Cost"
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
        "cost_overrun_estimate": round(float(cost_overrun), 2)
    }
