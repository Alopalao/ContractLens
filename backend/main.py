from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import connect_db, close_db
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.documents import router as documents_router
from app.security import get_password_hash


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = await connect_db()

    # Ensure default admin account exists
    admin = await db.users.find_one({"username": "admin"})
    if not admin:
        await db.users.insert_one(
            {
                "full_name": "Administrator",
                "email": "admin@contractlens.local",
                "username": "admin",
                "password": get_password_hash("admin"),
                "address": None,
                "phone": None,
                "created_at": datetime.utcnow(),
            }
        )
        print("✓ Default admin account created  (username: admin | password: admin)")
    elif "password" not in admin:
        await db.users.update_one(
            {"_id": admin["_id"]},
            {
                "$set": {"password": get_password_hash("admin")},
                "$unset": {"hashed_password": ""},
            },
        )

    yield

    close_db()


app = FastAPI(
    title="ContractLens API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(documents_router)


@app.get("/")
async def root():
    return {"message": "ContractLens API", "version": "1.0.0"}
