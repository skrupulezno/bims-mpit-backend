from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app import models, schemas, auth
from app.database import SessionLocal
from app.auth import create_access_token, create_refresh_token, decode_token, get_password_hash, verify_password
from slowapi.util import get_remote_address
from fastapi_limiter.depends import RateLimiter
from app.schemas import LoginSchema
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone_number == phone).first()

def authenticate_user(db: Session, phone: str, password: str):
    user = get_user(db, phone)
    if not user or not auth.verify_password(password, user.hashed_password, user.pepper):
        return None
    return user

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Неавторизован")
    payload = auth.decode_token(token)
    if not payload or payload.get("token_type") != "access":
        raise HTTPException(status_code=401, detail="Неверный или просроченный токен")
    phone = payload.get("sub")
    user = get_user(db, phone)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if get_user(db, user.phone):
        raise HTTPException(status_code=400, detail="Телефон уже зарегистрирован")
    
    new_user = models.User(
        phone_number=user.phone,
        first_name=user.first_name,    
        last_name=user.last_name     
    )
    if not new_user.pepper:
        new_user.pepper = uuid.uuid4().hex

    new_user.hashed_password = auth.get_password_hash(user.password, new_user.pepper)
    new_user.system_role = "guest"
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"msg": "Пользователь успешно зарегистрирован"}

@router.post("/login", dependencies=[Depends(RateLimiter(times=5, seconds=300))])
async def login(response: Response, request: Request, form_data: LoginSchema, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.phone, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Неверный телефон или пароль")
    
    access_token = create_access_token(data={"sub": user.phone_number})
    refresh_token = create_refresh_token(data={"sub": user.phone_number})

    expires_at = datetime.utcnow() + timedelta(days=auth.settings.refresh_token_expire_days)
    new_session = models.Session(
        user_id=user.id,
        refresh_token=refresh_token,
        expires_at=expires_at
    )
    db.add(new_session)
    db.commit()
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=auth.settings.access_token_expire_minutes * 60,
        secure=True,
        samesite="lax"
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=auth.settings.refresh_token_expire_days * 24 * 3600,
        secure=True,
        samesite="lax"
    )
    return {"msg": "Вход выполнен успешно"}

@router.post("/refresh")
async def refresh_access_token(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Отсутствует refresh токен")
    
    payload = auth.decode_token(refresh_token)
    if not payload or payload.get("token_type") != "refresh":
        raise HTTPException(status_code=401, detail="Неверный или просроченный refresh токен")
    
    session_record = db.query(models.Session).filter(models.Session.refresh_token == refresh_token).first()
    if not session_record:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    if session_record.expires_at < datetime.utcnow():
        db.delete(session_record)
        db.commit()
        raise HTTPException(status_code=401, detail="Сессия истекла")
    
    phone = payload.get("sub")
    new_access_token = create_access_token(data={"sub": phone})
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        max_age=auth.settings.access_token_expire_minutes * 60,
        secure=True,
        samesite="lax"
    )
    return {"msg": "Access токен обновлен"}

@router.post("/logout")
async def logout(response: Response, request: Request, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        session_record = db.query(models.Session).filter(models.Session.refresh_token == refresh_token).first()
        if session_record:
            db.delete(session_record)
            db.commit()
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"msg": "Вы вышли из системы"}

@router.get("/protected")
async def protected_route(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    return {"msg": f"Привет, {current_user.phone_number}"}

@router.get("/active_sessions")
async def get_active_sessions(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    now = datetime.utcnow()
    active_sessions = db.query(models.Session).filter(
        models.Session.user_id == current_user.id,
        models.Session.expires_at > now
    ).all()
    
    results = []
    for session in active_sessions:
        results.append({
            "phone": current_user.phone_number,
            "started_at": session.created_at.isoformat()
        })
    return results

@router.delete("/active_sessions/{session_id}")
async def delete_active_session(
    session_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session_obj = db.query(models.Session).filter(
        models.Session.id == session_id,
        models.Session.user_id == current_user.id
    ).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    
    db.delete(session_obj)
    db.commit()
    return {"msg": "Сессия успешно удалена"}