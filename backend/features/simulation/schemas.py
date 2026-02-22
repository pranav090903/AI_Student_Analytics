from pydantic import BaseModel
from features.prediction.schemas import StudentData

class SimulationRequest(BaseModel):
    student: StudentData
    new_attendance: float
    new_quiz: float
