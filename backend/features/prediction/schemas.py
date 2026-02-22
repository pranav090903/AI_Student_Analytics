from pydantic import BaseModel
class StudentData(BaseModel):
    attendance_percentage: float 
    assignment_avg:float
    quiz_avg:float
    midterm_score:float
    previous_semester_score:float