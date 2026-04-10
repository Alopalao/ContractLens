import io
from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from app.security import get_current_user
from app.database import get_db
from app.services.gemini import analyze_contract

router = APIRouter(prefix="/api/documents", tags=["documents"])

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


async def _extract_text(file: UploadFile) -> str:
    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 10 MB)")

    name = (file.filename or "").lower()

    if name.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")

    if name.endswith(".pdf"):
        try:
            from pypdf import PdfReader

            reader = PdfReader(io.BytesIO(content))
            return "\n".join(
                page.extract_text() or "" for page in reader.pages
            )
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Cannot read PDF: {exc}")

    if name.endswith(".docx"):
        try:
            import docx

            doc = docx.Document(io.BytesIO(content))
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Cannot read DOCX: {exc}")

    raise HTTPException(
        status_code=400,
        detail="Unsupported file type. Please upload PDF, DOCX, or TXT.",
    )


@router.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    text = await _extract_text(file)
    if not text.strip():
        raise HTTPException(status_code=400, detail="No text could be extracted from the file.")

    try:
        analysis = await analyze_contract(text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}")

    db = get_db()
    doc = {
        "user_id": str(current_user["_id"]),
        "filename": file.filename,
        "preview_text": text[:2000],
        "document_text": text[:50000],
        "analysis": analysis,
        "created_at": datetime.utcnow(),
    }
    result = await db.documents.insert_one(doc)

    return {
        "id": str(result.inserted_id),
        "filename": file.filename,
        "analysis": analysis,
        "created_at": doc["created_at"],
    }


@router.get("/")
async def list_documents(current_user=Depends(get_current_user)):
    db = get_db()
    docs = (
        await db.documents.find(
            {"user_id": str(current_user["_id"])},
            {"preview_text": 0},
        )
        .sort("created_at", -1)
        .to_list(100)
    )
    return [
        {
            "id": str(d["_id"]),
            "filename": d["filename"],
            "analysis": d.get("analysis"),
            "created_at": d["created_at"],
        }
        for d in docs
    ]


@router.get("/{doc_id}")
async def get_document(doc_id: str, current_user=Depends(get_current_user)):
    db = get_db()
    try:
        obj_id = ObjectId(doc_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid document ID")

    doc = await db.documents.find_one(
        {"_id": obj_id, "user_id": str(current_user["_id"])}
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "id": str(doc["_id"]),
        "filename": doc["filename"],
        "analysis": doc.get("analysis"),
        "created_at": doc["created_at"],
        "preview_text": doc.get("preview_text"),
        "document_text": doc.get("document_text"),
    }


@router.delete("/{doc_id}")
async def delete_document(doc_id: str, current_user=Depends(get_current_user)):
    db = get_db()
    try:
        obj_id = ObjectId(doc_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid document ID")

    result = await db.documents.delete_one(
        {"_id": obj_id, "user_id": str(current_user["_id"])}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"message": "Document deleted"}
