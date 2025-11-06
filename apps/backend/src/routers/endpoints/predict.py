from fastapi import APIRouter
from src.services.prediction_service import prediction_service
from src.schemas.request_schema import SensorData

router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("/classification")
def compute_classification_prediction(sensor_data: SensorData):
    """
    Returns classification prediction based on sensor data.
    """
    return prediction_service.classification_prediction(sensor_data)

@router.post("/regression")
def compute_regression_prediction(sensor_data: dict):
    """
    Returns regression prediction (RUL) based on sensor data.
    """
    pass

@router.post("/")
def compute_predictions(sensor_data: dict):
    """
    Compute both predictions.
    """
    pass


    

