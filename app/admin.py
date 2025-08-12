from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter()


class SettingsPayload(BaseModel):
    modelType: str
    riskThreshold: float


# In-memory settings store (replace with DB later)
CURRENT_SETTINGS = {
    "modelType": "xgboost",
    "riskThreshold": 0.5,
}


@router.post("/admin/settings")
def update_settings(payload: SettingsPayload):
    rt = float(payload.riskThreshold)
    # Accept 0..1 or 0..10 scales; normalize to 0..1
    if not (0 <= rt <= 1 or 0 <= rt <= 10):
        raise HTTPException(status_code=400, detail="Invalid threshold")
    if rt > 1:
        rt = rt / 10.0

    CURRENT_SETTINGS.update({
        "modelType": payload.modelType,
        "riskThreshold": rt,
    })
    return {"ok": True, "settings": CURRENT_SETTINGS}


@router.post("/admin/retrain")
def retrain_model():
    # TODO: hook to real training pipeline
    return {"ok": True, "message": "Retraining started (mock)"}


class ValidationPayload(BaseModel):
    projectId: str
    action: str  # "validate" | "correct" | "cancel"


@router.post("/admin/validate")
def validate_prediction(payload: ValidationPayload):
    if payload.action not in {"validate", "correct", "cancel"}:
        raise HTTPException(status_code=400, detail="Invalid action")
    # TODO: write to DB audit_logs / predictions status
    return {"ok": True, "projectId": payload.projectId, "action": payload.action}


