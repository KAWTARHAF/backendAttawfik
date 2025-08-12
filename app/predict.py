from fastapi import APIRouter, HTTPException
from app.shemas import ProjectInput
from app.ml_models import predict_project_outcomes

router = APIRouter()

@router.post("/predict")
def predict(input_data: ProjectInput):
    """
    Receives project input and returns ML predictions
    (delay probability, risk level, and estimated cost overrun).
    """
    try:
        result = predict_project_outcomes(input_data.dict())
        return result
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
