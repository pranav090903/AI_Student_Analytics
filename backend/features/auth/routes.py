from fastapi import APIRouter, HTTPException
from infrastructure.database import users_collection
from features.auth.password_utils import hash_password, verify_password
from features.auth.jwt_handler import create_access_token
from features.auth.schemas import RegisterUser, LoginUser

router = APIRouter(prefix="/auth", tags=["Auth"])


# ================= REGISTER =================

@router.post("/register")
def register(user: RegisterUser):
    print(f"[INFO] Registration Request: {user.model_dump()}")

    existing = users_collection.find_one({"username": user.username})

    if existing:
        print(f"[WARN] Registration Failed: User '{user.username}' already exists.")
        raise HTTPException(400, "User already exists")

    users_collection.insert_one({
        "username": user.username,
        "password": hash_password(user.password),
        "role": user.role
    })

    return {"message": "User registered successfully"}


# ================= LOGIN =================

@router.post("/login")
def login(user: LoginUser):
    print(f"[INFO] Login Request for user: {user.username}")

    db_user = users_collection.find_one({"username": user.username})

    if not db_user:
        print(f"[WARN] Login Failed: Username '{user.username}' not found.")
        raise HTTPException(400, "Invalid username")

    if not verify_password(user.password, db_user["password"]):
        print(f"[WARN] Login Failed: Incorrect password for '{user.username}'.")
        raise HTTPException(400, "Invalid password")

    token = create_access_token({
        "username": user.username,
        "role": db_user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user["role"]
    }
