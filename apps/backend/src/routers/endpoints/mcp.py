from fastapi import APIRouter, HTTPException
from src.services.machine_state_service import get_machine_state

router = APIRouter(prefix="/mcp", tags=["MCP"])

@router.get("/status/{machine_id}")
def get_status(machine_id: int):
    state = get_machine_state(machine_id)

    if state is None:
        raise HTTPException(status_code=404, detail="Machine state not found. Run simulation first.")

    return {
        "machineID": machine_id,
        "timestamp": state.get("timestamp"),
        "prediction": state.get("prediciton", {}),
        "features": state.get("features", {}),
        "mcp_events": state.get("mcp_events", [])
    }
