class LogService:
    def __init__(self):
        self.logs = []

    def create_alert(self, machine_id, failure_prob):
         self.logs.append({
            "type": "alert",
            "machine_id": machine_id,
            "probability": failure_prob
        })
    
    def create_work_order(self, machine_id, rul_hours):
         self.logs.append({
            "type": "work_order",
            "machine_id": machine_id,
            "rul_hours": rul_hours
        })
    
    def log_event(self, message: str):
        """
        Append to internal log list.
        """
        self.logs.append(message)
    
    def get_logs(self):
        return self.logs
    
log_service = LogService()