from src.schemas.request_schema import SensorData

class FeatureEngineering:
    """
    Service class for feature engineering
    """
    def _get_features(sensor_data: SensorData):
        """
        Temporary class for feature creation simulation.
        """
        volt = sensor_data['volt']  # 0.126322196
        rotate = sensor_data['rotate'] # -1.66442733
        pressure = sensor_data['pressure'] # -0.3250084191
        vibration = sensor_data['vibration'] # -1.144192998
        age = sensor_data['age'] # 0.4581633938
        
        {"volt":volt,"rotate":rotate,"pressure":pressure,"vibration":vibration,"age":age,
         "error1":-0.0343470023,"error2":-0.0336187405,"error3":-0.0311350082,"error4":-0.0285806449,"error5":-0.0206257354,"maint_comp1":-0.0282177945,"maint_comp2":-0.0295730269,"maint_comp3":-0.0282421291,"maint_comp4":-0.0285565978,"has_maintenance":-0.0495992318,"has_failure":-0.0288200154,"volt_rolling_6h_mean":0.1683755111,"volt_rolling_6h_std":2.119008697,"volt_rolling_24h_mean":0.6188846436,"volt_rolling_24h_std":1.111677369,"rotate_rolling_6h_mean":-2.519499127,"rotate_rolling_6h_std":1.209279297,"rotate_rolling_24h_mean":-4.625549762,"rotate_rolling_24h_std":1.032672337,"pressure_rolling_6h_mean":0.2269541309,"pressure_rolling_6h_std":-1.001590979,"pressure_rolling_24h_mean":0.2910486444,"pressure_rolling_24h_std":0.1893806003,"vibration_rolling_6h_mean":-0.3043916696,"vibration_rolling_6h_std":-1.171288584,"vibration_rolling_24h_mean":-0.6695767984,"vibration_rolling_24h_std":-1.116335253,"volt_lag_1h":1.829425924,"volt_lag_3h":2.004322186,"volt_change_1h":-1.254352745,"rotate_lag_1h":-2.043133163,"rotate_lag_3h":-0.6016700813,"rotate_change_1h":0.2892745898,"pressure_lag_1h":0.3940953652,"pressure_lag_3h":-0.5783744898,"pressure_change_1h":-0.5600455436,"vibration_lag_1h":0.3775849049,"vibration_lag_3h":-0.1904805704,"vibration_change_1h":-1.154363258,"error_count_last_24_h":2.85105063,"hours_since_last_error":-0.9101899604,"hours_since_last_maintenance":0.4282813345,"days_since_last_failure":-0.431880157,"total_errors_to_date":2.79730675,"total_maintenances_to_date":1.704669696,"total_failures_to_date":1.09917074,"model2":-0.4525696379,"model3":-0.7337993857,"model4":1.457737974,"age_squared":0.2644651639,"volt_deviation_from_machine_avg":0.1363677766,"rotate_deviation_from_machine_avg":-1.657856613,"pressure_deviation_from_machine_avg":-0.3042737074,"vibration_deviation_from_machine_avg":-1.162631222}


    def create_features(sensor_data: SensorData):
        """
        Creates & returns  all remaining features.
        """
        pass
