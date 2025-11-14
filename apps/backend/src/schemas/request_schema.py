from pydantic import BaseModel

class SensorData(BaseModel):
    volt: float
    pressure: float
    rotate: float
    vibration: float
    age: int

