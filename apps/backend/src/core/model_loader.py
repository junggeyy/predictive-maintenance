import joblib
import os

# moving 5 levels up, to the project root
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
MODEL_DIR = os.path.join(BASE_DIR, "models")

_classification_model = None
_regression_model = None

def get_classification_model():
    global _classification_model
    if _classification_model is None:
        print("Classification model being loaded.")
        model_path = os.path.join(MODEL_DIR, "random_forest_final.pkl")
        _classification_model = joblib.load(model_path)
        print(f"Classification model loaded from {model_path}")
        
    return _classification_model

def get_regression_model():
    pass
