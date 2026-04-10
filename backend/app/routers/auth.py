from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
from datetime import datetime

from app.models import UserRegister, UserLogin, Token
from app.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _user_out(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "full_name": user["full_name"],
        "email": user["email"],
        "username": user["username"],
        "address": user.get("address"),
        "phone": user.get("phone"),
    }


@router.post("/register", response_model=Token)
async def register(user_data: UserRegister):
    db = get_db()

    existing = await db.users.find_one(
        {"$or": [{"username": user_data.username}, {"email": user_data.email}]}
    )
    if existing:
        field = "Username" if existing.get("username") == user_data.username else "Email"
        raise HTTPException(status_code=400, detail=f"{field} already in use")

    doc = {
        "full_name": user_data.full_name,
        "email": user_data.email,
        "username": user_data.username,
        "password": get_password_hash(user_data.password),
        "address": None,
        "phone": None,
        "created_at": datetime.utcnow(),
    }
    result = await db.users.insert_one(doc)
    doc["_id"] = result.inserted_id

    token = create_access_token(
        {"sub": user_data.username},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=token, token_type="bearer", user=_user_out(doc))


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    db = get_db()
    user = await db.users.find_one({"username": credentials.username})

    stored_password = user.get("password") if user else None
    if not user or not stored_password or not verify_password(credentials.password, stored_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token(
        {"sub": user["username"]},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=token, token_type="bearer", user=_user_out(user))


@router.get("/me")
async def get_me(current_user=Depends(get_current_user)):
    return {
        **_user_out(current_user),
        "created_at": current_user.get("created_at"),
    }
