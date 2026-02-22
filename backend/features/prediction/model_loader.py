import joblib
import os

# Get path to the models directory within the prediction feature
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "random_forest_model.pkl")

model = None

if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print(f"[OK] Model loaded successfully from {MODEL_PATH}")
    except Exception as e:
        print(f"[ERROR] Error loading model: {e}")
else:
    print(f"[WARNING] Model file not found at {MODEL_PATH}")
    print("Please ensure the 'random_forest_model.pkl' is placed in backend/features/prediction/models/")
