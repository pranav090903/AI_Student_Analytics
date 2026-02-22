
import sys
import os
import time

# Add backend to path
backend_path = os.path.join(os.getcwd(), "backend")
sys.path.append(backend_path)

try:
    from copilot.chat_service import copilot_chat
    from database.mongodb import student_records_collection
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)

# 1. Setup Test Data (2 Students)
print("Setting up test data...")
student_1 = {
    "student_id": "student_strong",
    "student_username": "student_strong",
    "attendance_percentage": 95.0,
    "assignment_avg": 90.0,
    "quiz_avg": 92.0,
    "midterm_score": 88.0, 
    "risk_level": "Safe"
}
student_2 = {
    "student_id": "student_weak",
    "student_username": "student_weak",
    "attendance_percentage": 20.0,
    "assignment_avg": 30.0,
    "quiz_avg": 40.0,
    "midterm_score": 25.0,
    "risk_level": "Critical"
}

student_records_collection.update_one({"student_id": "student_strong"}, {"$set": student_1}, upsert=True)
student_records_collection.update_one({"student_id": "student_weak"}, {"$set": student_2}, upsert=True)

# 2. Test Class Analysis
print("\nAttempting class analysis chat...")
try:
    message = "Who is the weakest student in the class?"
    print(f"Teacher Message: {message}")
    
    response = copilot_chat(
        role="Teacher",
        message=message,
        username="teacher_test"
    )
    
    print("\nCopilot Response:")
    print(response)
    
    # Verify
    if "student_weak" in response or "weak" in response.lower():
        print("\nSUCCESS: Copilot identified the weakest student.")
    else:
        print("\nWARNING: Copilot might not have identified the correct student.")

except Exception as e:
    print("\nRETURNED ERROR:")
    print(e)
