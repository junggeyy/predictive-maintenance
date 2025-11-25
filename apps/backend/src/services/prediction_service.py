from src.core.model_loader import get_classification_model, get_regression_model
import pandas as pd

class PredictionService:
    """
    Prediction service class.
    """
    def __init__(self):
        self.classifier, self.classifier_scaler = get_classification_model()
        self.regressor, self.regressor_scaler = get_regression_model()

    def predict_failure(self, features: dict):
        """
        Runs classification model.
        Returns:
            probability of failure
            predicted_label (0 or 1)
        """
        feature_names = list(self.classifier_scaler.feature_names_in_)
        
        # converting features dict to ordered df
        X_df = pd.DataFrame([[features[f] for f in feature_names]], columns=feature_names)

        # scale the data
        X_scaled = self.classifier_scaler.transform(X_df)
        X = pd.DataFrame(X_scaled, columns=feature_names)

        # get prediction
        failure_prob = float(self.classifier.predict_proba(X)[0][1])
        failure_label = int(self.classifier.predict(X)[0])

        return failure_prob, failure_label

    def predict_rul(self, features: dict):
        """
        Runs regression model.
        Returns:
            predicted RUL hours
        """
        feature_names = list(self.regressor_scaler.feature_names_in_)
        
        # work around for naming mismatch
        if "error_count_last_24_h" in features:
            features["error_count_last_24h"] = features.pop("error_count_last_24_h")

        # converting features dict to ordered df
        X_df = pd.DataFrame([[features[f] for f in feature_names]], columns=feature_names)

        # scale the data
        X_scaled = self.regressor_scaler.transform(X_df)
        X = pd.DataFrame(X_scaled, columns=feature_names)

        # get prediction
        rul_prediction = float(self.regressor.predict(X)[0])

        return rul_prediction
    
prediction_service = PredictionService()    