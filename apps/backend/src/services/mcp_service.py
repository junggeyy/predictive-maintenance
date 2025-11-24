class MCPService:
    def __init__(self):
        self.logs = []

    def create_alert(self, machine_id, failure_prob):
        pass
    
    def create_work_order(self, machine_id, rul_hours):
        pass
    
    def log_event(self, message: str):
        """
        Append to internal MCP log list.
        """
        self.logs.append(message)
    
    def get_logs(self):
        return self.logs
    
mcp_service = MCPService()