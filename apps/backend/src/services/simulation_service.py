from src.services.feature_engineering_service import feature_engineering_service
from src.services.prediction_service import prediction_service
from src.services.mcp_service import mcp_service

class SimulationService:
    """
    Simulation service class for production pipeline simulation. 
    """

    def start_simulation(self, df):
        """
        Runs the simulation on provided df by:
            - Extracting required features
            - For each machine row:
                - get classification prediction
                - if machine is failing -> regression prediction & trigger MCP alerts
            - Returns the full simulation results
        """
        engineered_df = feature_engineering_service.extract_features(df)
    
        simulation_results = []
        for idx, row in engineered_df.iterrows(): # try random rows 
            # classification
            fail_prob, fail_label = prediction_service.predict_failure(row)
            
            if fail_label == 1:
                # regression with alert & work-order
                rul = prediction_service.predict_rul(row)
                mcp_service.create_alert(row["machineID"], fail_prob)
                mcp_service.create_work_order(row["machineID"], rul)
            else:
                rul = None
            
            result = {
                "row_index": idx,
                "machineID": row["machineID"],
                "failure_prob": fail_prob,
                "failure_label": fail_label,
                "rul": rul,
                "timestamp": row["datetime"],
                "mcp_events": mcp_service.get_logs()
            }
            print(f"Prediction for {idx}: {fail_label}")
            
            if fail_label == 1:
                simulation_results.append(result)

        return simulation_results

simulation_service = SimulationService()