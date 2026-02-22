import os
import sys

# Ensure backend directory is in the sys path so internal imports like 'from features...' work
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from fastapi import FastAPI, Depends
import pandas as pd

from features.prediction.schemas import StudentData
from features.copilot.schemas import CopilotRequest
from features.simulation.schemas import SimulationRequest

from features.prediction.model_loader import model
from features.copilot.service import student_copilot_chat, teacher_copilot_chat
from features.simulation.service import simulate_student
from features.auth.routes import router as auth_router
from features.auth.dependencies import get_current_user
from features.student_records.routes import router as record_router
from features.copilot.routes import router as copilot_router


app = FastAPI(title="EduPulse AI: Student Success Platform")
app.include_router(auth_router)
risk_map = {0: "Safe", 1: "At Risk", 2: "Critical"}

app.include_router(record_router)
app.include_router(copilot_router)

@app.get("/")
def home():
    return {"message": "EduPulse AI Backend Running"}


@app.get("/protected-test")
def protected_test(user = Depends(get_current_user)):
    return {
        "message": "You are authenticated",
        "user": user
    }

@app.post("/predict")
def predict(data: StudentData):

    if model is None:
        return {"error": "ML Model not loaded on server. Please ensure random_forest_model.pkl is in backend/features/prediction/models/"}

    df = pd.DataFrame([data.model_dump()])

    pred = model.predict(df)[0]
    proba = model.predict_proba(df)[0]
    conf = float(proba[pred])

    return {
        "prediction": risk_map[pred],
        "confidence": conf,
        "accuracy": 0.925
    }


@app.post("/copilot-chat")
def copilot_api(req: CopilotRequest):

    if model is None:
        return {"error": "ML Model not loaded on server. Please ensure random_forest_model.pkl is in backend/features/prediction/models/"}

    student_dict = req.student.model_dump()

    df = pd.DataFrame([student_dict])
    pred = model.predict(df)[0]
    proba = model.predict_proba(df)[0]
    conf = float(proba[pred])

    response = student_copilot_chat(
        student_data=student_dict,
        prediction=risk_map[pred],
        confidence=conf,
        question=req.question
    )

    return {
        "prediction": risk_map[pred],
        "confidence": conf,
        "accuracy": 0.925,
        "copilot_response": response
    }


@app.post("/simulate")
def simulation_api(req: SimulationRequest):

    return simulate_student(
        original_student=req.student.model_dump(),
        new_attendance=req.new_attendance,
        new_quiz=req.new_quiz
    )
