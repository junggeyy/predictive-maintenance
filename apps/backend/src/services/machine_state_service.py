# This is our in-memory state store during runtime
MACHINE_STATE = {}

def set_machine_state(machine_id: int, data: dict):
    MACHINE_STATE[machine_id] = data

def get_machine_state(machine_id: int):
    return MACHINE_STATE.get(machine_id)
