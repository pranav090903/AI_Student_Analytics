from pydantic import BaseModel
class StudentRecord(BaseModel):
    student_id: str
    attendance_percentage: float
    assignment_avg: float
    quiz_avg: float
    midterm_score: float
    previous_semester_score: float
