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
async def create_or_update_profile(
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
