from mcp.types import Tool, ToolSchema
import requests

FASTAPI_URL = "http://localhost:8000" 

def get_machine_status(machine_id: int):
    url = f"{FASTAPI_URL}/machine/status/{machine_id}"
    r = requests.get(url)

    if r.status_code != 200:
        return {"error": f"Machine {machine_id} not found or simulation not run."}

    return r.json()

TOOLS = [
    Tool(
        name="get_machine_status",
        description="Returns the latest sensor, engineered features, and prediction results for a machine.",
        input_schema=ToolSchema(
            type="object",
            properties={
                "machine_id": {"type": "integer"},
            },
            required=["machine_id"]
        ),
        func=get_machine_status
    )
]
