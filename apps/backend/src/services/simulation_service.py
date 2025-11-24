from src.services.feature_engineering_service import feature_engineering_service
from src.services.prediction_service import prediction_service
from src.services.mcp_service import mcp_service

class SimulationService:
    """
    Simulation service class for production pipeline simulation. 
    """

    def start_simulation(self, df):
        """
        1. Extract engineered features
        2. Loop through each machine row
        3. Classification prediction
        4. If fail → regression RUL prediction
        5. Trigger MCP alerts
        6. Yield or return results
        """
        engineered_df = feature_engineering_service.extract_features(df)
        rul = None

        fail_prob, fail_label = prediction_service.predict_failure(engineered_df)
        if fail_label == 1:
            rul = prediction_service.predict_rul(engineered_df)

        result = {
                "failure_prob": fail_prob,
                "failure_label": fail_label,
                "rul": rul,
                "mcp_events": mcp_service.get_logs()
            }
        
        return result
    
        # simulation_results = []
        # for idx, row in engineered_df.iterrows():
            
        #     # classification
        #     fail_prob, fail_label = prediction_service.predict_failure(row)
            
        #     if fail_label == 1:
        #         rul = prediction_service.predict_rul(row)
        #         mcp_service.create_alert(row["machineID"], fail_prob)
        #         mcp_service.create_work_order(row["machineID"], rul)
        #     else:
        #         rul = None
            
        #     result = {
        #         "row_index": idx,
        #         "machineID": row["machineID"],
        #         "failure_prob": fail_prob,
        #         "failure_label": fail_label,
        #         "rul": rul,
        #         "timestamp": row["datetime"],
        #         "mcp_events": mcp_service.get_logs()
        #     }

        #     simulation_results.append(result)

        # return simulation_results

simulation_service = SimulationService()