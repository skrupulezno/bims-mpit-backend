from fastapi import File, Request, UploadFile
from fastapi.responses import FileResponse

@router.get("/documents/{doc_id}")
def download_document(doc_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")
    return FileResponse(document.file_path, media_type="application/octet-stream", filename=document.title)
