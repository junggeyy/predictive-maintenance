import joblib
import os

# moving 5 levels up, to the project root
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
MODEL_DIR = os.path.join(BASE_DIR, "models")

_classification_model = None
_classification_scaler = None
_regression_model = None
_regression_scaler = None

def get_classification_model():
    """
    Lazily loads and returns the classification model and its corresponding scaler.
    Ensures both model & scaler are only loaded once at startup, and reuses exisiting instances.
    """
    global _classification_model, _classification_scaler

    if _classification_model is None:
        model_path = os.path.join(MODEL_DIR, "random_forest_final.pkl")
        _classification_model = joblib.load(model_path)
        print(f"Classification model loaded.")

    if _classification_scaler is None:
        print("Classification scaler being loaded.")
        model_path = os.path.join(MODEL_DIR, "classification_scaler.pkl")
        _classification_scaler = joblib.load(model_path)
        print(f"Classification scaler loaded.")
        
    return _classification_model, _classification_scaler

def get_regression_model():
    pass
