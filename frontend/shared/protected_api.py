import requests

BASE_URL = "http://127.0.0.1:8002"


def protected_test_api(token):

    return requests.get(
        f"{BASE_URL}/protected-test",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
