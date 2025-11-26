"""
Helper functions for MCP server tool implementations
"""
import requests

FASTAPI_URL = "http://localhost:8000" 

def get_machine_status(machine_id: int):
    """
    Query the FastAPI backend for machine status.
    Returns JSON with machine prediction data and features.
    """
    url = f"{FASTAPI_URL}/mcp/status/{machine_id}"
    
    try:
        r = requests.get(url, timeout=5)
        
        if r.status_code != 200:
            return {"error": f"Machine {machine_id} not found or simulation not run."}
        
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to connect to backend: {str(e)}"}
