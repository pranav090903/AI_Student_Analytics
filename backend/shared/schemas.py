from pydantic import BaseModel
from typing import List


class StudentGenAIOutput(BaseModel):
    status: str
    reasons: List[str]
    suggestions: List[str]


class TeacherGenAIOutput(BaseModel):
    status: str
    academic_causes: List[str]
    teacher_actions: List[str]


class AdminGenAIOutput(BaseModel):
    status: str
    key_risk_drivers: List[str]
    institutional_suggestions: List[str]
