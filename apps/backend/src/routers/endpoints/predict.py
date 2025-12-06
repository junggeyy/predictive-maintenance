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
def compute_classification_prediction(features: dict):
    """
    Returns classification prediction.
    """
    return prediction_service.predict_failure(features)

@router.post("/regression")
def compute_regression_prediction(features: dict):
    """
    Returns regression prediction (RUL).
    """
    return prediction_service.predict_rul(features)



    

