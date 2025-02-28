from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
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
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    
    if profile_data.photo_url is not None:
        profile.photo_url = profile_data.photo_url
    if profile_data.additional_info is not None:
        profile.additional_info = profile_data.additional_info
    
    if profile.user:
        if hasattr(profile_data, "first_name") and profile_data.first_name is not None:
            profile.user.first_name = profile_data.first_name
        if hasattr(profile_data, "last_name") and profile_data.last_name is not None:
            profile.user.last_name = profile_data.last_name
    
    db.commit()
    db.refresh(profile)
    
    result = {
        "id": profile.id,
        "user_id": profile.user_id,
        "photo_url": profile.photo_url,
        "additional_info": profile.additional_info,
        "user": {
            "first_name": profile.user.first_name,
            "last_name": profile.user.last_name
        } if profile.user else None,
    }
    return result


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

    result = {
        "id": profile.id,
        "user_id": profile.user_id,
        "business_role": profile.business_role,
        "corporate_email": profile.corporate_email,
        "photo_url": profile.photo_url,
        "additional_info": profile.additional_info,
        "department_id": profile.department_id,
        "user": {
            "first_name": current_user.first_name,
            "last_name": current_user.last_name
        },
        "department": {
            "id": profile.department.id,
            "name": profile.department.name
        } if profile.department else None
    }
    return result

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
    
    result = {
        "id": profile.id,
        "user_id": profile.user_id,
        "business_role": profile.business_role,
        "corporate_email": profile.corporate_email,
        "photo_url": profile.photo_url,
        "additional_info": profile.additional_info,
        "department_id": profile.department_id,
        "user": {
            "first_name": profile.user.first_name,
            "last_name": profile.user.last_name
        } if profile.user else None,
        "department": {
            "id": profile.department.id,
            "name": profile.department.name
        } if profile.department else None
    }
    return result

@router.get("/profiles")
async def get_all_profiles(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.system_role != "admin":
        raise HTTPException(status_code=403, detail="Доступ только для администраторов")
    
    profiles = db.query(models.EmployeeProfile).all()
    results = []
    for profile in profiles:
        results.append({
            "id": profile.id,
            "user_id": profile.user_id,
            "business_role": profile.business_role,
            "corporate_email": profile.corporate_email,
            "photo_url": profile.photo_url,
            "additional_info": profile.additional_info,
            "department_id": profile.department_id,
            "user": {
                "first_name": profile.user.first_name,
                "last_name": profile.user.last_name
            } if profile.user else None,
            "department": {
                "id": profile.department.id,
                "name": profile.department.name
            } if profile.department else None
        })
    return results
