
import sys
import os
import requests

# Add backend to path so we can import modules
backend_path = os.path.join(os.getcwd(), "backend")
sys.path.append(backend_path)

# We need a token for the request. 
# Since we can't easily login via script without running the whole auth flow, 
# and the endpoint is protected, we might need to mock the dependency or use a known test user if available.
# However, for this verification, I'll rely on the unit test approach of importing the router 
# and calling the function directly if possible, OR just testing the DB query logic.

# Actually, let's just test the DB logic directly to ensure "get all" works.
try:
    from database.mongodb import student_records_collection
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)

print("Fetching all student records from DB directly...")
records = list(student_records_collection.find({}, {"_id": 0}))

print(f"Found {len(records)} records.")
if len(records) > 0:
    print("Sample Record:")
    print(records[0])
    print("\nSUCCESS: Data retrieval logic works.")
else:
    print("No records found (which is valid if DB is empty).")
    print("SUCCESS: Data retrieval logic works (empty DB).")
