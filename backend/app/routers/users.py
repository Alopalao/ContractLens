from fastapi import APIRouter, Depends, HTTPException

from app.models import UserUpdate
from app.security import get_current_user
from app.database import get_db

router = APIRouter(prefix="/api/users", tags=["users"])


@router.put("/me")
async def update_profile(update_data: UserUpdate, current_user=Depends(get_current_user)):
    db = get_db()

    fields = {k: v for k, v in update_data.model_dump().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    await db.users.update_one({"_id": current_user["_id"]}, {"$set": fields})

    updated = await db.users.find_one({"_id": current_user["_id"]})
    return {
        "id": str(updated["_id"]),
        "full_name": updated["full_name"],
        "email": updated["email"],
        "username": updated["username"],
        "address": updated.get("address"),
        "phone": updated.get("phone"),
    }
