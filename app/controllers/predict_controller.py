from app.model.predictor import predict_project_outcomes


def make_prediction(data: dict) -> dict:
    """
    Business logic layer: handles prediction workflow.

    Args:
        data (dict): The input data for the project (validated).

    Returns:
        dict: Prediction results from the ML models.
    """
    return predict_project_outcomes(data)
