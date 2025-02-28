from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.profile import generate_corporate_email
from app.routes.auth_routes import get_current_user

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/profile")
async def update_profile(
    profile_data: schemas.ProfileCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.system_role == "guest":
        raise HTTPException(status_code=403, detail="Гостевой пользователь не может изменять профиль")
    
    profile = db.query(models.EmployeeProfile).filter(models.EmployeeProfile.user_id == current_user.id).first()
    if profile:
        profile.first_name = profile_data.first_name
        profile.last_name = profile_data.last_name
        profile.additional_info = profile_data.additional_info
        db.commit()
        return {"msg": "Профиль обновлен"}
    else:
        raise HTTPException(status_code=404, detail="Профиль не найден")


@router.get("/profile")
async def get_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.system_role == "guest":
        raise HTTPException(status_code=403, detail="Гостевой пользователь не имеет профиля")
    
    profile = db.query(models.EmployeeProfile).filter(models.EmployeeProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    return profile

@router.get("/profile/{profile_id}")
async def get_profile_by_id(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.system_role != "admin":
        raise HTTPException(status_code=403, detail="Доступ только для администраторов")
    
    profile = db.query(models.EmployeeProfile).filter(models.EmployeeProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    
    return profile

@router.get("/profiles")
async def get_all_profiles(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.system_role != "admin":
        raise HTTPException(status_code=403, detail="Доступ только для администраторов")
    
    profiles = db.query(models.EmployeeProfile).all()
    return profiles
