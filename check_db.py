from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["ai_student_db"]
users = list(db["users"].find({}, {"password": 0}))

print("--- Current Registered Users info (No Passwords) ---")
for u in users:
    print(u)
print("--------------------------------------------------")
