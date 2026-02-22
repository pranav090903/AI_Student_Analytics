import requests

BACKEND_URL = "http://127.0.0.1:8002"


def predict_api(student_data):
    return requests.post(f"{BACKEND_URL}/predict", json=student_data)


def copilot_api(payload):
    return requests.post(f"{BACKEND_URL}/copilot-chat", json=payload)


def simulate_api(payload):
    return requests.post(f"{BACKEND_URL}/simulate", json=payload)
