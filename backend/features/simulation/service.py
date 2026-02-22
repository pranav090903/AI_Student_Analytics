import pandas as pd
from features.prediction.model_loader import model
from infrastructure.ai.simulation_chain import simulation_chain

risk_map = {0: "Safe", 1: "At Risk", 2: "Critical"}

def simulate_student(original_student, new_attendance, new_quiz):

    if model is None:
        return {"error": "ML Model not loaded on server. Please ensure random_forest_model.pkl is in backend/features/prediction/models/"}

    original_df = pd.DataFrame([original_student])
    original_pred = model.predict(original_df)[0]

    modified = original_student.copy()
    modified["attendance_percentage"] = new_attendance
    modified["quiz_avg"] = new_quiz

    new_df = pd.DataFrame([modified])
    new_pred = model.predict(new_df)[0]

    explanation = simulation_chain.invoke({
        "original_prediction": risk_map[original_pred],
        "new_prediction": risk_map[new_pred]
    })

    return {
        "original": risk_map[original_pred],
        "new": risk_map[new_pred],
        "simulation_explanation": explanation
    }
