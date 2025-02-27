from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.routes.auth_routes import get_current_user
from datetime import datetime

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def get_published_news(db: Session = Depends(get_db)):
    news_list = db.query(models.News).filter(models.News.is_approved == True).order_by(models.News.created_at.desc()).all()
    return news_list

@router.post("/")
async def create_news(news_data: schemas.NewsCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.system_role not in ["employee", "admin"]:
        raise HTTPException(status_code=403, detail="Недостаточно прав для создания новости")
    new_news = models.News(
        title=news_data.title,
        content=news_data.content,
        news_type=news_data.news_type,
        author_id=current_user.id,
        is_approved=True if current_user.system_role=="admin" else False,
        created_at=datetime.utcnow()
    )
    db.add(new_news)
    db.commit()
    db.refresh(new_news)
    return {"msg": "Новость создана", "news_id": new_news.id, "approved": new_news.is_approved}

@router.put("/{news_id}/approve")
async def approve_news(news_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.system_role != "admin":
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    news_item = db.query(models.News).filter(models.News.id == news_id).first()
    if not news_item:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    news_item.is_approved = True
    db.commit()
    return {"msg": "Новость одобрена"}

@router.delete("/{news_id}")
async def delete_news(news_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    news_item = db.query(models.News).filter(models.News.id == news_id).first()
    if not news_item:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    if current_user.system_role != "admin" and news_item.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав для удаления")
    db.delete(news_item)
    db.commit()
    return {"msg": "Новость удалена"}
