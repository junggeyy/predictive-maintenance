from fastapi import APIRouter, HTTPException
from apps.backend.src.services.machine_state_service import get_machine_state

router = APIRouter(prefix="/mcp", tags=["MCP"])

@router.get("/status/{machine_id}")
def get_status(machine_id: int):
    state = get_machine_state(machine_id)

    if state is None:
        raise HTTPException(status_code=404, detail="Machine state not found. Run simulation first.")

    return state
