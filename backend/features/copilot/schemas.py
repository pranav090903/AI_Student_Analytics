from pydantic import BaseModel
from features.prediction.schemas import StudentData

class CopilotRequest(BaseModel):
    student: StudentData
    question: str

class TeacherChatRequest(BaseModel):
    message: str
