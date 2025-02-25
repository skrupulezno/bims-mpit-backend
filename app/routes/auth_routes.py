from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app import models, schemas, auth, database
from app.profile import generate_corporate_email

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone_number == phone).first()

def authenticate_user(db: Session, phone: str, password: str):
    user = get_user(db, phone)
    if not user or not auth.verify_password(password, user.hashed_password):
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

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if get_user(db, user.phone):
        raise HTTPException(status_code=400, detail="Телефон уже зарегистрирован")

    new_user = models.User(
        phone_number=user.phone,
        hashed_password=auth.get_password_hash(user.password),
        system_role="guest"  
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"msg": "Пользователь успешно зарегистрирован"}

@router.post("/login")
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Неверный телефон или пароль")
    
    access_token = auth.create_access_token(data={"sub": user.phone_number})
    refresh_token = auth.create_refresh_token(data={"sub": user.phone_number})

    expires_at = datetime.utcnow() + timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS)
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
        max_age=auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=auth.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
    )
    return {"msg": "Вход выполнен успешно"}

@router.post("/profile")
def create_or_update_profile(
    profile_data: schemas.ProfileCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) 
):
    if current_user.system_role == "guest":
        raise HTTPException(status_code=403, detail="Гостевой пользователь не может создавать или изменять профиль")
    
    profile = db.query(models.EmployeeProfile).filter(models.EmployeeProfile.user_id == current_user.id).first()
    if profile:
        profile.first_name = profile_data.first_name
        profile.last_name = profile_data.last_name
        profile.additional_info = profile_data.additional_info
        db.commit()
        return {"msg": "Профиль обновлен"}
    else:
        full_name = f"{profile_data.first_name} {profile_data.last_name}"
        corporate_email = generate_corporate_email(db, full_name)
        new_profile = models.EmployeeProfile(
            user_id=current_user.id,
            first_name=profile_data.first_name,
            last_name=profile_data.last_name,
            corporate_email=corporate_email,
            additional_info=profile_data.additional_info
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return new_profile

@router.get("/profile")
def get_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.system_role == "guest":
        raise HTTPException(status_code=403, detail="Гостевой пользователь не имеет профиля")
    
    profile = db.query(models.EmployeeProfile).filter(models.EmployeeProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    return profile

@router.patch("/users/{user_id}/upgrade")
def upgrade_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.system_role != "admin":
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if target_user.system_role != "guest":
        raise HTTPException(status_code=400, detail="Можно обновить только роль гостя")
    
    target_user.system_role = "employee"
    db.commit()
    

    if not target_user.profile:
        corporate_email = generate_corporate_email(db, target_user.phone_number)
        new_profile = models.EmployeeProfile(
            user_id=target_user.id,
            first_name="",  # Здесь можно подставить ФИО, если оно было сохранено
            last_name="",
            corporate_email=corporate_email
        )
        db.add(new_profile)
        db.commit()
    
    return {"msg": "Роль пользователя обновлена на работник"}


@router.get("/protected")
def protected_route(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    return {"msg": f"Привет, {current_user.phone_number}"}



@router.post("/refresh")
def refresh_access_token(request: Request, response: Response, db: Session = Depends(get_db)):
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
    new_access_token = auth.create_access_token(data={"sub": phone})
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        max_age=auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return {"msg": "Access токен обновлен"}

@router.post("/logout")
def logout(response: Response, request: Request, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        session_record = db.query(models.Session).filter(models.Session.refresh_token == refresh_token).first()
        if session_record:
            db.delete(session_record)
            db.commit()
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"msg": "Вы вышли из системы"}

@router.get("/active_sessions")
def get_active_sessions(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    active_sessions = db.query(models.Session).filter(models.Session.expires_at > now).all()
    
    results = []
    for session in active_sessions:
        results.append({
            "phone": session.user.phone_number,
            "started_at": session.created_at
        })
    return results

@router.post("/profile")
def create_or_update_profile(
    profile_data: schemas.ProfileCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    profile = db.query(models.EmployeeProfile).filter(models.EmployeeProfile.user_id == current_user.id).first()
    if profile:
        profile.first_name = profile_data.first_name
        profile.last_name = profile_data.last_name
        profile.additional_info = profile_data.additional_info
        db.commit()
        return {"msg": "Профиль обновлен"}
    else:
        full_name = f"{profile_data.first_name} {profile_data.last_name}"
        corporate_email = generate_corporate_email(db, full_name)
        new_profile = models.EmployeeProfile(
            user_id=current_user.id,
            first_name=profile_data.first_name,
            last_name=profile_data.last_name,
            corporate_email=corporate_email,
            additional_info=profile_data.additional_info
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return new_profile

@router.get("/profile")
def get_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    profile = db.query(models.EmployeeProfile).filter(models.EmployeeProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    return profile

@router.patch("/users/{user_id}/upgrade")
def upgrade_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.system_role != "admin":
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if target_user.system_role != "guest":
        raise HTTPException(status_code=400, detail="Можно обновить только роль гостя")
    
    target_user.system_role = "employee"
    db.commit()
    return {"msg": "Роль пользователя обновлена на работник"}