from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

db = client["ai_student_db"]

users_collection = db["users"]
student_records_collection = db["student_records"]
