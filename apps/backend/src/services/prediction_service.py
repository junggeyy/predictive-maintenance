class PredictionService:
    """
    Prediction service class.
    """
    def __init__(self):
        pass

    def classification_prediction(self, data: dict):
        return {"data": data, "prediction": "Your machine is cooked."}

    def regression_prediction(self, data: dict):
        pass
    
prediction_service = PredictionService()