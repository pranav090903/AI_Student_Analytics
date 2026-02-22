import sys
import os

# Add backend to path so we can import modules
backend_path = os.path.join(os.getcwd(), "backend")
sys.path.append(backend_path)

try:
    from copilot.chat_service import copilot_chat
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)

print("Attempting teacher chat...")
try:
    # Mimic the call from routes/copilot_route.py
    response = copilot_chat(
        role="Teacher",
        message="Hello, detailed academic advice please.",
        username="teacher_test"
    )
    print("Response:", response)
except Exception as e:
    print("Caught expected error:")
    print(e)
