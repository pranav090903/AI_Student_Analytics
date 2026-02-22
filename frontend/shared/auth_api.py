import requests

BASE_URL = "http://127.0.0.1:8002"


def login_api(username, password):
    return requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "username": username,
            "password": password
        }
    )


def register_api(username, password, role):
    return requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": username,
            "password": password,
            "role": role
        }
    )
