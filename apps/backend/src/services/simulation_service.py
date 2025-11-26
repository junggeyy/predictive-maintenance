from src.services.feature_engineering_service import feature_engineering_service
from src.services.prediction_service import prediction_service
from src.services.log_service import log_service
from src.services.machine_state_service import set_machine_state
import numpy as np
import pandas as pd

class SimulationService:
    """
    Simulation service class for production pipeline simulation. 
    """

    def select_representative_rows(self, df_engineered, num_failures=10):
        """
        Returns a representative row for each machine with at least num_failures failure cases.
        """
        machine_ids = df_engineered["machineID"].unique()

        # machine with at least one failure event
        failing_machines = df_engineered[df_engineered["target_failure_24h"] == 1]["machineID"].unique()
        selected_fail_machines = np.random.choice(
            failing_machines, size=num_failures, replace=False
        )

        selected_rows = []
        for m_id in machine_ids:
            df_machine = df_engineered[df_engineered["machineID"] == m_id]

            if m_id in selected_fail_machines:
                fail_rows = df_machine[df_machine["target_failure_24h"] == 1]

                if fail_rows.empty:
                    row = df_machine.sample(1)
                else:
                    row = fail_rows.sample(1)

            else:
                ok_rows = df_machine[df_machine["target_failure_24h"] == 0]

                if ok_rows.empty:
                    row = df_machine.sample(1)
                else:
                    row = ok_rows.sample(1)

            selected_rows.append(row)

        final_df = pd.concat(selected_rows, ignore_index=True)
        return final_df

    def start_simulation(self, df):
        """
        Runs the simulation on provided df by:
            - Extracting required features
            - Selects a representative row for each machine (100 rows)
            - For each machine row:
                - get classification prediction
                - if machine is failing -> regression prediction & trigger MCP alerts
            - Returns the full simulation results
        """
        engineered_df = feature_engineering_service.extract_features(df)
        sample_df = self.select_representative_rows(engineered_df)
    
        simulation_results = []
        for _, row in sample_df.iterrows():
            machine_id = int(row["machineID"])
            features = row.to_dict()

            # classification
            fail_prob, fail_label = prediction_service.predict_failure(features)
            
            if fail_label == 1:
                # regression with alert & work-order
                rul = prediction_service.predict_rul(features)
                log_service.create_alert(machine_id, fail_prob)
                log_service.create_work_order(machine_id, rul)
            else:
                rul = None
            
            result = {
                "machineID": machine_id,
                "timestamp": row["datetime"],
                "features": features,
                "prediciton": {
                    "failure_prob": fail_prob,
                    "failure_label": fail_label,
                    "rul": rul,
                },
                "mcp_events": log_service.get_logs()
            }
            
            set_machine_state(machine_id, result)
            simulation_results.append(result)

        return simulation_results

simulation_service = SimulationService()