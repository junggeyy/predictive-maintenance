from fastapi import APIRouter
from src.services.simulation_service import simulation_service
from src.services.prediction_service import prediction_service
from src.core.data_loader import data_loader

router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("/start")
def run_simulation():
    """
    Run full pipeline simulation.
    """
    df_test = data_loader.load_test_dataset()
    results = simulation_service.start_simulation(df_test)

    return {"results": results}

@router.post("/classification")
def compute_classification_prediction(sensor_data):
    """
    Returns classification prediction based on sensor data.
    """
    return prediction_service.classification_prediction(sensor_data)

@router.post("/regression")
def compute_regression_prediction(sensor_data):
    """
    Returns regression prediction (RUL) based on sensor data.
    """
    pass



    

