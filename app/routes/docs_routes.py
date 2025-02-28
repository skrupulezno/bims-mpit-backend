from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database
from fastapi.responses import FileResponse
import os

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/documents/{doc_id}")
async def download_document(doc_id: int, db: Session = Depends(get_db)):
    document = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")
    file_path = os.path.join("storage", document.file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")
    return FileResponse(file_path, media_type="application/octet-stream", filename=document.title)

