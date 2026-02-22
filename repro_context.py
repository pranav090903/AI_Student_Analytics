
import sys
import os
from datetime import datetime

# Add backend to path so we can import modules
backend_path = os.path.join(os.getcwd(), "backend")
sys.path.append(backend_path)

try:
    from copilot.chat_service import copilot_chat
    from database.mongodb import student_records_collection
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)

# 1. Setup Dummy Student
test_student_id = "test_student_context_123"
dummy_record = {
    "student_id": test_student_id,
    "attendance_percentage": 10.5, # Very low to be obvious
    "assignment_avg": 95.0,
    "quiz_avg": 88.0,
    "midterm_score": 92.0,
    "previous_semester_score": 90.0,
    "risk_level": "At Risk",
    "confidence_score": 0.85,
    "updated_by": "test_script",
    "updated_at": datetime.utcnow()
}

print(f"Upserting test student: {test_student_id} with 10.5% attendance...")
student_records_collection.update_one(
    {"student_id": test_student_id},
    {"$set": dummy_record},
    upsert=True
)

# 2. Test Chat
print("\nAttempting teacher chat with student context...")
try:
    # Message mentions the student ID
    message = f"What is the attendance of {test_student_id}?"
    print(f"Teacher Message: {message}")
    
    response = copilot_chat(
        role="Teacher",
        message=message,
        username="teacher_test"
    )
    print("\nCopilot Response:")
    print(response)
    
    # Simple verification
    if "10.5" in response or "low" in response.lower():
        print("\nSUCCESS: Copilot seems to have used the context.")
    else:
        print("\nWARNING: Copilot might not have used the context.")
        print(f"Response was: {response}")

except Exception as e:
    print("\nRETURNED ERROR:")
    print(e)
