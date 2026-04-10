from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.models import ChatRequest, ChatResponse
from app.security import get_current_user
from app.services.gemini import chat_with_documents

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(payload: ChatRequest, current_user=Depends(get_current_user)):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    db = get_db()
    user_id = str(current_user["_id"])

    query = {"user_id": user_id}
    if payload.document_ids:
        object_ids = []
        for doc_id in payload.document_ids:
            try:
                object_ids.append(ObjectId(doc_id))
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid document ID in selection")
        query["_id"] = {"$in": object_ids}

    documents = await db.documents.find(query).sort("created_at", -1).to_list(20)
    if not documents:
        raise HTTPException(
            status_code=400,
            detail="No documents available for chat. Analyze at least one document first.",
        )

    answer = await chat_with_documents(
        question=payload.message,
        documents=documents,
        history=[item.model_dump() for item in payload.history],
    )

    return ChatResponse(
        answer=answer,
        referenced_documents=[
            {"id": str(doc["_id"]), "filename": doc.get("filename", "Untitled")}
            for doc in documents
        ],
    )