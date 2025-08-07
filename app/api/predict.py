from fastapi import APIRouter, HTTPException
from app.schemas.project_input import ProjectInput
from app.controllers.predict_controller import make_prediction

router = APIRouter()

@router.post("/predict")
def predict(input_data: ProjectInput):
    """
    Receives project input and returns ML predictions
    (delay probability, risk level, and estimated cost overrun).
    """
    try:
        # Send validated input to the controller
        result = make_prediction(input_data.dict())
        return result
    except ValueError as ve:
        # Handle missing fields or input errors
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        # General error handling
        raise HTTPException(status_code=500, detail=str(e)) 
