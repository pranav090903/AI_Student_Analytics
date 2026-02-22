from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
import pandas as pd

# Auth
from features.auth.dependencies import get_current_user

# DB
from infrastructure.database import student_records_collection as db

# Schema
from features.student_records.schemas import StudentRecord 

# Model
from features.prediction.model_loader import model


router = APIRouter(prefix="/records", tags=["Student Records"])


# ==============================
# ADD OR UPDATE STUDENT RECORD
# ==============================
@router.post("/upsert")
def add_or_update_record(
    record: StudentRecord,
    user=Depends(get_current_user)
):
    """
    Teacher can add/update student academic record
    Also runs ML prediction and stores result
    """

    try:
        # ======================
        # ROLE CHECK
        # ======================
        if user["role"].lower() != "teacher":
            raise HTTPException(
                status_code=403,
                detail="Only teachers can add student records"
            )

        # ======================
        # PREPARE MODEL INPUT
        # ======================
        input_df = pd.DataFrame([{
            "attendance_percentage": record.attendance_percentage,
            "assignment_avg": record.assignment_avg,
            "quiz_avg": record.quiz_avg,
            "midterm_score": record.midterm_score,
            "previous_semester_score": record.previous_semester_score
        }])

        # ======================
        # MODEL PREDICTION
        # ======================
        if model is None:
            raise HTTPException(
                status_code=500,
                detail="ML Model not loaded on server. Please ensure random_forest_model.pkl is in backend/features/prediction/models/"
            )

        prediction = int(model.predict(input_df)[0])
        probability = float(model.predict_proba(input_df).max())

        # Label Mapping
        label_map = {
            0: "Safe",
            1: "At Risk",
            2: "Critical"
        }

        risk_label = label_map.get(prediction, "Unknown")

        # ======================
        # SAVE TO DATABASE
        # ======================
        model_accuracy = 0.925

        record_data = {
            "student_id": record.student_id,
            "attendance_percentage": record.attendance_percentage,
            "assignment_avg": record.assignment_avg,
            "quiz_avg": record.quiz_avg,
            "midterm_score": record.midterm_score,
            "previous_semester_score": record.previous_semester_score,
            "risk_level": risk_label,
            "confidence_score": probability,
            "model_accuracy": model_accuracy,
            "updated_by": user["username"],
            "updated_at": datetime.utcnow()
        }

        # Upsert → Update if exists else Insert
        db.update_one(
            {"student_id": record.student_id},
            {"$set": record_data},
            upsert=True
        )

        # ======================
        # RESPONSE
        # ======================
        return {
            "message": "Record saved successfully",
            "student_id": record.student_id,
            "prediction": risk_label,
            "confidence": round(probability, 3),
            "accuracy": model_accuracy
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/my-record")
def get_my_record(user=Depends(get_current_user)):
    """
    Student gets their own record
    """
    record = db.find_one(
        {"student_id": user["username"]},
        {"_id": 0}
    )

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
        
    return record


# ==============================
# GET STUDENT RECORD
# ==============================
@router.get("/{student_id}")
def get_student_record(
    student_id: str,
    user=Depends(get_current_user)
):
    """
    Student → Can view own record
    Teacher → Can view any record
    """

    record = db.find_one(
        {"student_id": student_id},
        {"_id": 0}
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    # Student can only see own record
    if user["role"].lower() == "student" and user["username"] != student_id:
        raise HTTPException(
            status_code=403,
            detail="Not allowed to view this record"
        )

    return record


# ==============================
# GET ALL STUDENT RECORDS
# ==============================
@router.get("/all/students")
def get_all_student_records(
    user=Depends(get_current_user)
):
    """
    Teacher → Can view all student records
    """

    # Role Check
    if user["role"].lower() != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Only teachers can view all records"
        )

    # Fetch all records
    records = list(db.find({}, {"_id": 0}))

    return records


# ==============================
# DELETE STUDENT RECORD
# ==============================
@router.delete("/{student_id}")
def delete_student_record(
    student_id: str,
    user=Depends(get_current_user)
):
    """
    Teacher can delete any student record
    """
    # Role Check
    if user["role"].lower() != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Only teachers can delete records"
        )

    result = db.delete_one({"student_id": student_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    return {"message": f"Record for {student_id} deleted successfully"}
